#!/usr/bin/env python3

import os

import crash_test.error_codes
from crash_test.error_logger import log_error


def instance_name_check(instance_name) -> bool:
    """
    Check if the provided instance name is valid
    :param instance_name: the name of the multipass instance
    :return: Bool: False if the provided instance name is not valid;
                   True if the provided instance name is valid.
    """
    if "_" in instance_name:
        correct_format: str = instance_name.replace("_", "-")
        print(f"{log_error(error_code=crash_test.error_codes.INVALID_INSTANCE_NAME_ERROR)}{correct_format}.")
        return False
    else:
        return True


def project_check(project_path) -> bool:
    """
    Check if the provided project is in the pwd and exists
    :param project_path: project name
    :return: Bool: False if the provided project is a single file.
                   True if the provided project exists.
    """
    if os.path.isfile(project_path):
        # if project_path is a file will return False
        print(log_error(error_code=crash_test.error_codes.SINGLE_FILE_ERROR))
        return False

    if os.path.exists(project_path):
        return True
    else:
        print(log_error(error_code=crash_test.error_codes.NO_SUCH_FILE_OR_DIRECTORY_ERROR, project_path=project_path))
        return False


def arguments_check(instance_name, project_path) -> bool:
    """
    Check the instance name format and project
    :return: bool: True if the checks pass;
                   False if the checks fails.
    """
    return instance_name_check(instance_name) and project_check(project_path)
