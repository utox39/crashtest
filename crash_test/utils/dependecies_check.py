#!/usr/bin/env python3

import os

from script_generator import script_generator


def check_dependencies(project_path: str) -> str:
    project_name = project_path[project_path.rfind("/") + 1:]
    for element in os.listdir(project_path):
        if element == "requirements.txt":
            return script_generator(project_name=project_name, project_type="python")
