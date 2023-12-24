#!/usr/bin/env python3

from colorama import Fore, Style

import crash_test.error_codes


def log_error(error_code: int, project_path: str = "", script_path: str = "") -> str:
    match error_code:
        case crash_test.error_codes.NO_SUCH_FILE_OR_DIRECTORY_ERROR:
            return f"crashtest: error: cannot access {project_path}: No such file or directory."
        case crash_test.error_codes.SINGLE_FILE_ERROR:
            return "Please only provide project directories. Single files are not allowed."
        case crash_test.error_codes.MULTIPASS_GENERIC_ERROR:
            return f"{Fore.RED}multipass: error: "
        case crash_test.error_codes.MULTIPASS_NOT_INSTALLED_ERROR:
            return "crashtest: error: Multipass is not installed!"
        case crash_test.error_codes.INVALID_INSTANCE_NAME_ERROR:
            return "crashtest: error: invalid instance name. The instance name should be like this: "
        case crash_test.error_codes.NO_DEPENDENCIES_FOUND_ERROR:
            return f"{Fore.YELLOW}No dependencies detected.{Style.RESET_ALL}\n"
        case crash_test.error_codes.NO_SUPPORTED_REQUIREMENTS_FILE_FOUND_ERROR:
            return f"{Fore.YELLOW}No supported project requirements file was found!{Style.RESET_ALL}\n"
        case crash_test.error_codes.SCRIPT_FOLDER_NOT_FOUND_ERROR:
            return f"crashtest: error: cannot access {script_path}: No such file or directory."
