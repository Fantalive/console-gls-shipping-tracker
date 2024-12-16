# Parcel Tracker

## Description

Parcel Tracker is a command-line application for tracking parcels via the GLS API. It fetches parcel data, monitors status changes, and displays the information in a user-friendly format. It supports optional features such as notifications, data persistence, and configurable settings via command-line arguments.

## Features
- **Real-time parcel tracking** using the GLS API.
- **Enhanced output formatting** for easier readability.
- **Data persistence** in `parcel_data.json` (optional).
- **Configurable settings** via command-line arguments.
- **Logging** for operations and errors.
- **Notifications** for parcel status changes.
- **Daily summary** generation at the end of each day.
- **Graceful exit** handling with `Ctrl+C`.
- **Rate limiting** to prevent excessive API requests.
- **Multiple Languages** Allows swapping of words for different language users.


## Installation
#### Languages used / required:


<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
<img src="https://img.shields.io/badge/json-5E5C5C?style=for-the-badge&logo=json&logoColor=white" />

---

### Insatallation steps:
1. Clone the repository:
```sh
git clone https://github.com/yourusername/parcel_tracker.git cd parcel_tracker
```

2. Install dependencies:
```sh
pip install -r requirements.txt
```

3. Configure the application (Assuming it exists, otherwise run as normal):
- Edit `config.json` to set up your preferences such as API intervals, logging settings, and enabled features.
- You can also specify these via command-line arguments when running `main.py`.

## Usage
1. Run the application:

### CLI Usage: 
```sh
python main.py [--min_interval INT] [--max_interval INT] [--status_monitoring] [--data_persistence] [--log_level LEVEL] [--log_file FILE] [--retry_attempts INT] [--retry_delay INT] [--parcel_numbers NUM1 NUM2 ...]
``` 

- `--min_interval`: Minimum interval between API requests in seconds.
- `--max_interval`: Maximum interval between API requests in seconds.
- `--status_monitoring`: Enable monitoring of parcel status changes.
- `--data_persistence`: Save tracked parcel data to `parcel_data.json`.
- `--log_level`: Set logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- `--log_file`: Specify the log file path.
- `--retry_attempts`: Number of retry attempts on API failure.
- `--retry_delay`: Delay between retries in seconds.
- `--parcel_numbers`: Parcel numbers to track.

### Executable:
    Run as executable.
### Python Script: 
```sh
python main.py
```

## Examples
### To track specific parcels:
- CLI Usage:
```cmd
python main.py --parcel_numbers 1234567890 9876543210
```

### To enable data persistence and set a minimum interval:
```sh
python main.py --data_persistence --min_interval 30
```

### Example config.json:
```json
{
    "base_url": "https://gls-group.com/app/service/open/rest/GROUP/en/rstt028/",
    "parcel_numbers": [
        "12345678901"
    ],
    "postal_code": "40202",
    "data_persistence": false,
    "log_file": "tracker.log",
    "retry_attempts": 3,
    "retry_delay": 5,
    "min_interval": 1800,
    "max_interval": 3600,
    "log_level": "INFO",
    "status_monitoring": true
}
```

### Example Output:
```
==================================================
Parcel Tracking Data:
==================================================

Parcel Number:       12345678901
Postal Code:         40202
Product:             EuroBusinessParcel
Weight:              1.21 kg
Services:            FlexDeliveryService,
Current Status:      INTRANSIT
Last Updated:        2024-11-15 08:20:46
  - 2024-11-14 13:51:44: The parcel has left the parcel center. (Country, Warehouse Location)
  - 2024-11-14 13:51:44: The parcel was handed over to GLS. (Country, Warehouse Location)
  - 2024-11-12 06:38:55: The parcel data was entered into the GLS IT system; the parcel was not yet handed over to GLS. (Country, Warehouse Location)
==================================================
Time until next pull: 29 minutes and 59 seconds.
```

### Example tracker.log (Subject to change as of 11/11/2024):
> [!NOTE]
> Useful information that users should know, even when skimming content.

```
[2024-12-01 08:00:00] INFO: Program started. Tracking parcels: [12345678901].
[2024-12-01 08:00:00] INFO: Parcel 12345678901: Fetching data from GLS API.
[2024-12-01 08:00:02] INFO: Parcel 12345678901: Status updated to PREADVICE. "The parcel data was entered into the GLS IT system; the parcel was not yet handed over to GLS."
[2024-12-01 09:30:00] INFO: Parcel 12345678901: Fetching data from GLS API.
[2024-12-01 09:30:01] INFO: Parcel 12345678901: Status remains unchanged (PREADVICE).

[2024-12-01 15:45:00] INFO: Parcel 12345678901: Fetching data from GLS API.
[2024-12-01 15:45:02] INFO: Parcel 12345678901: Status updated to INTRANSIT. "The parcel was handed over to GLS."

[2024-12-02 08:00:00] INFO: Parcel 12345678901: Fetching data from GLS API.
[2024-12-02 08:00:02] INFO: Parcel 12345678901: Status remains unchanged (INTRANSIT).

[2024-12-02 14:15:00] INFO: Parcel 12345678901: Fetching data from GLS API.
[2024-12-02 14:15:02] INFO: Parcel 12345678901: Status updated to OUT_FOR_DELIVERY. "The parcel has left the delivery center and is on its way to the recipient."

[2024-12-02 18:30:00] INFO: Parcel 12345678901: Fetching data from GLS API.
[2024-12-02 18:30:01] INFO: Parcel 12345678901: Status updated to DELIVERED. "The parcel was delivered successfully."

[2024-12-02 18:30:01] INFO: Parcel 12345678901: Completed delivery. Final status: DELIVERED.
[2024-12-02 18:30:01] INFO: Program execution completed. All parcels have reached a terminal status.

```

### Example parcel_data.json:
<details>
<summary>Example Code (Click here to show)</summary>
<pre>
{
    "postalCode": "POSTALCODE",
    "emailNotificationCard": false,
    "infos": [
        {
            "type": "WEIGHT",
            "name": "Weight:",
            "value": "1.21 kg"
        },
        {
            "type": "PRODUCT",
            "name": "Product:",
            "value": "EuroBusinessParcel"
        },
        {
            "type": "SERVICES",
            "name": "Services:",
            "value": "FlexDeliveryService,"
        }
    ],
    "owners": [
        {
            "type": "REQUEST",
            "code": "US01"
        },
        {
            "type": "DELIVERY",
            "code": "US01"
        }
    ],
    "references": [
        {
            "type": "UNITNO",
            "name": "Parcel number:",
            "value": "12345678901"
        },
        {
            "type": "GLSREF",
            "name": "Origin National Reference in Unicode",
            "value": "1234567890154321US"
        },
        {
            "type": "CUSTREF",
            "name": "Customer's own reference number",
            "value": "OCC1234567890154321"
        },
        {
            "type": "CUSTREF",
            "name": "Customers own reference number - per TU",
            "value": "OCC1234567890154321"
        }
    ],
    "history": [
        {
            "date": "2024-11-14",
            "time": "13:51:44",
            "evtDscr": "The parcel has left the parcel center.",
            "address": {
                "countryName": "COUNTRY NAME",
                "city": "CITY NAME",
                "countryCode": "COUNTRYCODE"
            }
        },
        {
            "date": "2024-11-14",
            "time": "13:51:44",
            "evtDscr": "The parcel was handed over to GLS.",
            "address": {
                "countryName": "COUNTRY NAME",
                "city": "CITY NAME",
                "countryCode": "COUNTRYCODE"
            }
        },
        {
            "date": "2024-11-12",
            "time": "06:38:55",
            "evtDscr": "The parcel data was entered into the GLS IT system; the parcel was not yet handed over to GLS.",
            "address": {
                "countryName": "COUNTRY NAME",
                "city": "CITY NAME",
                "countryCode": "COUNTRYCODE"
            }
        }
    ],
    "arrivalTime": {
        "name": "",
        "value": ""
    },
    "progressBar": {
        "level": 0,
        "retourFlag": false,
        "evtNos": [
            "1.0",
            "0.0",
            "0.100"
        ],
        "statusText": "In transit",
        "statusInfo": "INTRANSIT",
        "colourIndex": 0,
        "statusBar": [
            {
                "status": "PREADVICE",
                "imageStatus": "COMPLETE",
                "imageText": "Preadvice",
                "statusText": ""
            },
            {
                "status": "INTRANSIT",
                "imageStatus": "CURRENT",
                "imageText": "In transit",
                "statusText": "The parcel is on its way to the final parcel center.\nFor more information, please see the detailed shipment tracking below."
            },
            {
                "status": "INWAREHOUSE",
                "imageStatus": "PENDING",
                "imageText": "Final parcel center",
                "statusText": ""
            },
            {
                "status": "INDELIVERY",
                "imageStatus": "PENDING",
                "imageText": "In delivery",
                "statusText": ""
            },
            {
                "status": "DELIVERED",
                "imageStatus": "PENDING",
                "imageText": "Delivered",
                "statusText": ""
            }
        ]
    },
    "tuNo": "12345678901",
    "deliveryOwnerCode": "US01",
    "changeDeliveryPossible": false
}
</pre>
</details>

## Contributing
Feel free to submit issues and pull requests. Contributions are welcome!

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Link to MIT License:
[MIT License](https://opensource.org/licenses/MIT)