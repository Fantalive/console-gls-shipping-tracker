import json
import logging
import os

from datetime import datetime

from config import ARCHIVE_FILE


def generate_daily_summary(parcels_data):
    summary = f"Daily Summary - {datetime.now().strftime('%Y-%m-%d')}\n"
    summary += "-----------------------------------\n"

    for parcel, data in parcels_data.items():
        status = data.get("progressBar", {}).get("statusText", "Unknown")
        summary += f"Parcel {parcel}: {status}\n"

    logging.info(summary)
    print(summary)

    # Archive delivered parcels
    archive_delivered_parcels(parcels_data)



def archive_delivered_parcels(parcels_data):
    delivered = [
        {parcel: data}
        for parcel, data in parcels_data.items()
        if data.get("progressBar", {}).get("statusText", "").lower() == "delivered"
    ]

    if delivered:
        if os.path.exists(ARCHIVE_FILE):
            with open(ARCHIVE_FILE, "r") as file:
                archive = json.load(file)
        else:
            archive = []

        archive.extend(delivered)
        with open(ARCHIVE_FILE, "w") as file:
            json.dump(archive, file, indent=4)
        logging.info("Delivered parcels archived.")