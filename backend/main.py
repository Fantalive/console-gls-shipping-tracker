import logging
import signal
import sys
import argparse
import json

from config import config, update_config
from api import fetch_parcel_data_with_retry, monitor_status
from display import display_parcel_data
from utils import get_archive_path, get_config_path, get_random_interval, countdown
from daily_summary import generate_daily_summary

# Variables
parcels_data = {}

# Graceful exiting
def signal_handler(sig, frame):
    logging.info("Exiting program gracefully.")
    generate_daily_summary(parcels_data)
    print("\nExiting program. Goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Configure logging
logging.basicConfig(level=getattr(logging, config["log_level"].upper(), logging.INFO),
                    filename=config["log_file"],
                    format="%(asctime)s - %(levelname)s - %(message)s")

def reload_config():
    """
    Reload configuration from config.json if auto_reload_config is enabled.
    """
    try:
        config_path = get_config_path( "config.json" )
        with open( config_path, "r" ) as file:
            new_config = json.load(file)
            config.update(new_config)
            logging.info("Configuration reloaded successfully.")
    except Exception as e:
        logging.warning(f"Failed to reload configuration: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Track parcels via GLS API.")
    parser.add_argument("--min_interval", type=int, help="Minimum interval between API requests in seconds.")
    parser.add_argument("--max_interval", type=int, help="Maximum interval between API requests in seconds.")
    parser.add_argument("--status_monitoring", action="store_true", help="Enable status monitoring.")
    parser.add_argument("--data_persistence", action="store_true", help="Enable data persistence.")
    parser.add_argument("--log_level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level.")
    parser.add_argument("--log_file", help="Specify the log file path.")
    parser.add_argument("--retry_attempts", type=int, help="Number of retry attempts on failure.")
    parser.add_argument("--retry_delay", type=int, help="Delay in seconds between retries.")
    parser.add_argument("--parcel_numbers", nargs="*", help="Parcel numbers to track.")
    parser.add_argument("--auto_reload_config", action="store_true", help="Enable auto-reload of configuration.")
    parser.add_argument("--language", choices=["en", "es", "fr"], help="Set the language for the application.")
    
    return parser.parse_args()

def archive_delivered_parcels():
    """
    Archive delivered parcels into a separate JSON file.
    """
    delivered = [
        {parcel: data}
        for parcel, data in parcels_data.items()
        if data.get("progressBar", {}).get("statusText", "").lower() == "delivered"
    ]

    if delivered:
        config_path = get_archive_path( "archive.json" )
        
        try:
            with open( config_path, "r" ) as file:
                archive = json.load(file)
        except FileNotFoundError:
            archive = []

        archive.extend(delivered)
        with open( config_path , "w") as file:
            json.dump(archive, file, indent=4)
        logging.info("Delivered parcels archived.")

def main():

    global parcels_data

     # Parse command-line arguments
    args = parse_arguments()

    # Update config with command-line arguments if provided
    if args.min_interval:
        update_config("min_interval", args.min_interval)
    if args.max_interval:
        update_config("max_interval", args.max_interval)
    if args.status_monitoring:
        update_config("status_monitoring", True)
    if args.data_persistence:
        update_config("data_persistence", True)
    if args.log_level:
        update_config("log_level", args.log_level)
    if args.log_file:
        update_config("log_file", args.log_file)
    if args.retry_attempts:
        update_config("retry_attempts", args.retry_attempts)
    if args.retry_delay:
        update_config("retry_delay", args.retry_delay)
    if args.parcel_numbers:
        update_config("parcel_numbers", args.parcel_numbers)
    if args.language:
        update_config("language", args.language)

    try:
        while True:

            if config.get("auto_reload_config"):
                reload_config()

            for parcel_number in config["parcel_numbers"]:
                try:
                    data = fetch_parcel_data_with_retry(config["base_url"], parcel_number, config["postal_code"])
                    parcels_data[parcel_number] = data
                    monitor_status(data, parcel_number)
                    display_parcel_data(data)  # Improved display output for the fetched data
                except Exception as e:
                    logging.error(f"Error with parcel {parcel_number}: {e}")
                    print(f"Error: {e}")

            # Archive delivered parcels after every fetch cycle
            archive_delivered_parcels()

            interval = get_random_interval(config["min_interval"], config["max_interval"])
            countdown(interval)

    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()