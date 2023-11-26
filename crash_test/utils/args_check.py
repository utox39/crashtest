#!/usr/bin/env python3

import os


def instance_name_check(instance_name) -> bool:
    """
    Check if the provided instance name is valid
    :param instance_name: the name of the multipass instance
    :return: Bool: False if the provided instance name is not valid;
                   True if the provided instance name is valid.
    """
    if "_" in instance_name:
        correct_format: str = instance_name.replace("_", "-")
        print(f"crashtest: error: invalid instance name. The instance name should be like this: {correct_format}.")
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
        print("Please only provide project directories. Single files are not allowed.")
        return False

    if os.path.exists(project_path):
        return True
    else:
        print(f"crashtest: error: cannot access {project_path}: No such file or directory.")
        return False


def arguments_check(instance_name, project_path) -> bool:
    """
    Check the instance name format and project
    :return: bool: True if the checks pass;
                   False if the checks fails.
    """
    return instance_name_check(instance_name) and project_check(project_path)
