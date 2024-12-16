import requests
import time
import logging
import json

from config import config
from notifications import send_notification

last_request_time = 0

# Status Mapping Dictionary
STATUS_MAPPING = {
    "In delivery": "Your parcel is out for delivery.",
    "Delivered": "Your parcel has been successfully delivered.",
    "In transit": "Your parcel is on its way to the destination."
}

def save_data_to_file(data, filename="parcel_data.json"):
    if config.get("data_persistence"):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        logging.info("Data saved to file.")

def fetch_parcel_data_with_retry(base_url, parcel_number, postal_code):
    global last_request_time
    current_time = time.time()

    # Debug log
    logging.debug(f"Starting fetch for parcel {parcel_number} with postal code {postal_code}.")
    logging.debug(f"Last request time: {last_request_time}, Current time: {current_time}")

    # Enforce rate limiting
    if current_time - last_request_time < 30:
        delay = 30 - (current_time - last_request_time)
        logging.warning(f"Rate limiting: waiting {delay:.2f} seconds before next request.")
        time.sleep(delay)

    unix_time = int(current_time * 1000)
    url = f"{base_url}{parcel_number}?caller=witt002&millis={unix_time}&postalCode={postal_code}"
    logging.debug(f"Constructed API URL: {url}")

    for attempt in range(1, config["retry_attempts"] + 1):
        try:
            response = requests.get(url)
            response.raise_for_status()
            last_request_time = time.time()
            data = response.json()

            # Debug log response
            logging.debug(f"API Response for parcel {parcel_number}: {data}")

            # Save to file if persistence is enabled
            save_data_to_file(data)

            return data
        except requests.ConnectionError:
            logging.error("No internet connection.")
        except requests.HTTPError as e:
            logging.error(f"HTTP Error: {e.response.status_code}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        logging.warning(f"Retrying ({attempt}/{config['retry_attempts']}) after delay.")
        time.sleep(config["retry_delay"])
    raise Exception("Failed to fetch data after retries.")

def send_webhook_notification(parcel_number, status):
    if config.get("webhook_enabled", False):
        for webhook_url in config.get("webhook_urls", []):
            attempts = 3  # Retry attempts
            for attempt in range(1, attempts + 1):
                try:
                    payload = {"parcel_number": parcel_number, "status": status}
                    response = requests.post(webhook_url, json=payload)
                    response.raise_for_status()
                    logging.info(f"Webhook notification sent to {webhook_url} for parcel {parcel_number}.")
                    break  # Exit retry loop on success
                except Exception as e:
                    logging.error(f"Attempt {attempt}: Failed to send webhook to {webhook_url} - {e}")
                    if attempt == attempts:
                        logging.error(f"All attempts failed for webhook: {webhook_url}")

        
def monitor_status(data, parcel_number):
    if config["status_monitoring"]:
        status = data.get("progressBar", {}).get("statusText", "Unknown")
        if config.get("status_mapping", False):
            status = STATUS_MAPPING.get(status, status)

        # Send notifications
        if "In delivery" in status:
            send_notification("Parcel Tracker", f"Parcel {parcel_number} is now in delivery!")
            send_webhook_notification(parcel_number, status)
        elif "Delivered" in status:
            send_notification("Parcel Tracker", f"Parcel {parcel_number} has been delivered.")
            send_webhook_notification(parcel_number, status)