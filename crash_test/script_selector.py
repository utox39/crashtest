#!/usr/bin/env python3

import os


def script_selector(project_type: str, scripts_path) -> str:
    if os.path.exists(scripts_path):
        match project_type:
            case "python":
                return os.path.join(scripts_path, "python_dependencies.sh")
