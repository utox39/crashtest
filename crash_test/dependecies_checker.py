#!/usr/bin/env python3

import os
from typing import Final

from crash_test.error_logger import log_error
from crash_test.script_generator import script_generator

YELLOW: Final[str] = "\033[1m\033[33m"
NC: Final[str] = "\033[0m"


def check_dependencies(project_path: str) -> str:
    if os.path.exists(project_path):
        project_name = project_path[project_path.rfind("/") + 1:]
        for element in os.listdir(project_path):
            match element:
                case "requirements.txt":
                    return script_generator(project_name=project_name, project_type="python")
                case _:
                    print(log_error(error_code=306))
    else:
        print(log_error(error_code=300, project_path=project_path))
