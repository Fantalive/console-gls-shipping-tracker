import json
import logging
import os

from utils import get_archive_path, get_config_path, get_log_path, get_language_config_path

CONFIG_FILE = get_config_path("config.json")
LANGUAGES_FILE = get_language_config_path("languages.json")
ARCHIVE_FILE = get_archive_path("archive.json")
LOG_FILE = get_log_path("tracker.log")

# Default configuration
DEFAULT_CONFIG = {
    "base_url": "https://gls-group.com/app/service/open/rest/GROUP/en/rstt028/",
    "parcel_numbers": [],
    "postal_code": "12345",
    "data_persistence": False,
    "log_file": LOG_FILE,
    "log_level": "INFO",
    "archive_file": ARCHIVE_FILE,
    "retry_attempts": 3,
    "retry_delay": 5,
    "min_interval": 1800,
    "max_interval": 3600,
    "status_monitoring": True,
    "language": "en",
    "status_mapping": False,
    "webhook_enabled": False,
    "auto_reload_config": True,
    "webhook_urls": [
        "https://discord.com/webhook1",
        "https://backend.com/webhook2"
    ]
}

def load_or_create_config():
    """Load the configuration file or create one if it doesn't exist."""
    if not os.path.exists(CONFIG_FILE):
        print("No configuration file found. Let's set up the program.")
        setup_config()
    else:
        update_config_file_if_needed()

    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)
        
        # Load language configurations if languages.json exists
        if os.path.exists(LANGUAGES_FILE):
            with open(LANGUAGES_FILE, "r") as lang_file:
                languages_config = json.load(lang_file)
                config.update(languages_config)  # Merge configurations

    return config

def setup_config():
    """Interactively create a new configuration file."""
    config = DEFAULT_CONFIG.copy()
    config["postal_code"] = input("Enter your postal code: ").strip()
    num_parcels = int(input("How many parcels do you want to track? ").strip())
    for i in range(num_parcels):
        parcel = input(f"Enter parcel number {i + 1}: ").strip()
        config["parcel_numbers"].append(parcel)
    save_config(config)
    logging.info(f"Configuration saved to {CONFIG_FILE}.")
    print(f"Configuration saved to {CONFIG_FILE}.")

def update_config_file_if_needed():
    """Update the existing configuration file if it doesn't match the default structure."""
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    except json.JSONDecodeError:
        print("Error: Configuration file is corrupted. Recreating configuration.")
        logging.error("Error: Configuration file is corrupted. Recreating configuration.")
        setup_config()
        return

    updated = False
    for key, default_value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = default_value
            updated = True
            print(f"Added missing key '{key}' with default value: {default_value}")
    if updated:
        save_config(config)
        logging.info(f"Configuration file updated with new settings.")
        print(f"Configuration file updated with new settings.")

def save_config(config):
    """Save the updated configuration to the file."""
    logging.info("Config saved.")
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

def update_config(key, value):
    """Update a specific key in the configuration file."""
    config = load_or_create_config()
    config[key] = value
    save_config(config)

# Load the configuration at module import
config = load_or_create_config()
