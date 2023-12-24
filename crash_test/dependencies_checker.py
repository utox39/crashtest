#!/usr/bin/env python3

import os

import crash_test.error_codes
from crash_test.error_logger import log_error
from crash_test.script_selector import script_selector
from crash_test.utils import get_scripts_absolute_path, check_script_path


def find_requirements_file(project_path):
    if os.path.exists(project_path):
        files = [element for element in os.listdir(project_path) if element is not os.path.isdir(element)]
        for file in files:
            match file:
                case "requirements.txt":
                    return "python"


def check_dependencies(project_path: str, scripts_relative_path) -> str:
    if os.path.exists(project_path):
        project_type = find_requirements_file(project_path=project_path)
        scripts_absolute_path = get_scripts_absolute_path(relative_path=scripts_relative_path)
        if project_type:
            if check_script_path(script_path=scripts_absolute_path):
                return script_selector(project_type=project_type,
                                       scripts_path=scripts_absolute_path)
        else:
            print(log_error(error_code=crash_test.error_codes.NO_SUPPORTED_REQUIREMENTS_FILE_FOUND_ERROR))
    else:
        print(log_error(error_code=crash_test.error_codes.NO_SUCH_FILE_OR_DIRECTORY_ERROR, project_path=project_path))
