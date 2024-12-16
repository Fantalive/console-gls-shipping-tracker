import requests
import logging

from plyer import notification
from config import config

def send_notification(title, message):
    if config.get("status_monitoring"):
        notification.notify(
            title=title,
            message=message,
            app_name="Parcel Tracker",
            timeout=10  # Duration in seconds
        )

def send_webhook_notification(parcel_data):
    if not config.get("webhooks"):
        return
    for url in config["webhooks"]:
        try:
            response = requests.post(url, json=parcel_data, timeout=10)
            if response.status_code == 200:
                logging.info(f"Webhook sent successfully to {url}")
            else:
                logging.warning(f"Webhook failed with status {response.status_code} for {url}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send webhook to {url}: {e}")