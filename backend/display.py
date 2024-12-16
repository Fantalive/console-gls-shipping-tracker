import json
import os
import time

from colorama import Fore, init, Style

from config import config
from utils import get_language_config_path

init()

def get_translation(language):
    """Load translation file for the given language."""
    translations_path = get_language_config_path(f"translations_{language}.json")
    with open(translations_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_parcel_data(data):
    """Format parcel data for better display."""
    translations = get_translation(config["language"])
    
    output_lines = [
        Style.BRIGHT + f"{translations['parcel_number']:<30} " + Fore.GREEN + f"{data.get('references', [{'value': 'N/A'}])[0]['value']}",
        Style.RESET_ALL + Style.BRIGHT + f"{translations['postal_code']:<30} " + Fore.GREEN + f"{data.get('postalCode', 'N/A')}",
        Style.RESET_ALL + Style.BRIGHT + f"{translations['postage_type']:<30} " + Fore.CYAN + f"{data.get('infos', [{'value': 'N/A'}])[1]['value']}",
        Style.RESET_ALL + Style.BRIGHT + f"{translations['weight']:<30} " + Fore.RED + f"{data.get('infos', [{'value': 'N/A'}])[0]['value']}",
        Style.RESET_ALL + Style.BRIGHT + f"{translations['services']:<30} " + Fore.GREEN + f"{data.get('infos', [{'value': 'N/A'}])[2]['value']}",
        Style.RESET_ALL + Style.BRIGHT + f"{translations['current_status']:<30} " + Fore.CYAN + f"{data.get('progressBar', {'statusInfo': 'N/A'})['statusInfo']}",
        Style.RESET_ALL + Style.BRIGHT + f"{translations['last_updated']:<30} " + Fore.RED + f"{time.strftime('%Y-%m-%d %H:%M:%S')}",
        Style.RESET_ALL + Style.BRIGHT + Fore.RED + f"\n{translations['history']}:"
    ]
    
    history_entries = data.get('history', [])
    print()
    for entry in history_entries:
        output_lines.append( Fore.CYAN + f"  - {entry['date']} {entry['time']}: {entry['evtDscr']} ({translations['country']}: {entry['address']['countryName']}, {translations['city']}: {entry['address']['city']})")

    return "\n".join(output_lines)

def display_parcel_data(data):
    """Display the parcel tracking data in a readable format."""
    clear_console()

    translations = get_translation(config["language"])

    print("==================================================")
    print(f"{translations['parcel_tracking_data']}")
    print("==================================================")
    formatted_output = format_parcel_data(data)
    print(formatted_output)
    print()
    print(Style.RESET_ALL + "==================================================" + Style.RESET_ALL)