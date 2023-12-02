#!/usr/bin/env python3

import os

import crash_test.error_codes
from crash_test.error_logger import log_error
from crash_test.script_generator import script_generator


def check_dependencies(project_path: str) -> str:
    if os.path.exists(project_path):
        project_name = project_path[project_path.rfind("/") + 1:]
        for element in os.listdir(project_path):
            match element:
                case "requirements.txt":
                    return script_generator(project_name=project_name, project_type="python")
                case _:
                    print(log_error(error_code=crash_test.error_codes.NO_SUPPORTED_REQUIREMENTS_FILE_FOUND_ERROR))
    else:
        print(log_error(error_code=crash_test.error_codes.NO_SUCH_FILE_OR_DIRECTORY_ERROR, project_path=project_path))
