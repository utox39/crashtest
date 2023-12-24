#!/usr/bin/env python3

import os
import site
import sys

from colorama import Fore, Style

import crash_test.error_codes
from crash_test.error_logger import log_error


def get_scripts_absolute_path(relative_path):
    """
    Get the site-packages path and return the path to the scripts
    :return: script_path: the absolute path to the scripts
    """

    site_packages = ""
    if sys.platform.startswith("darwin"):
        site_packages = site.getsitepackages()[0]
    elif sys.platform.startswith("linux"):
        site_packages = site.getusersitepackages()
    elif sys.platform.startswith("win32"):
        site_packages = site.getsitepackages()[1]

    scripts_path = os.path.join(site_packages, relative_path)

    return scripts_path


def check_script_path(script_path) -> bool:
    if os.path.exists(script_path):
        return True
    else:
        print(log_error(error_code=crash_test.error_codes.SCRIPT_FOLDER_NOT_FOUND_ERROR, script_path=script_path))
        print(f"{Fore.RED}𝙓 Can not install dependencies!{Style.RESET_ALL}\n")
        return False
