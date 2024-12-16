import json
import os
import random
import time

from colorama import Fore, init, Style

init()


def get_random_interval(min_interval, max_interval):
    return random.randint(min_interval, max_interval)

def countdown(seconds):
    
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        print(Style.BRIGHT + Fore.GREEN + f"\rTime until next shipping update check: " + Style.BRIGHT + Fore.RED + f"{mins:02d} minutes and {secs:02d} seconds." + Style.RESET_ALL, end="")
        time.sleep(1)
        seconds -= 1
    print()

def get_project_root():
    """
    Return the root directory of the project.
    """
    return os.path.dirname( os.path.dirname( __file__ ))

def get_backend_path( filename ):
    """ Return the path to a file in the backend directory """
    return os.path.join( get_project_root(), "backend", filename )

def get_config_path( filename ):
    """ Return the path to a configuration file. """
    return os.path.join( get_project_root(), filename )

def get_language_config_path( filename ):
    """ Return the path to the language configuration file. """
    return os.path.join( get_project_root(), "translations", filename )

def get_archive_path( filename ):
    """ Return the path to archive file. """
    return os.path.join( get_project_root(), "archive", filename )

def get_log_path( filename ):
    """Return the path to the log file. """
    return os.path.join( get_project_root(), "logs", filename )