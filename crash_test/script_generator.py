#!/usr/bin/env python3

from typing import Final


def script_generator(project_name: str, project_type: str) -> str:
    script_content = ""
    commands: Final[dict] = {
        "python": [
            ['#!/usr/bin/env bash\n'],
            ['echo "Executing: sudo apt-get update"'],
            ['sudo apt-get update\n'],
            ['echo "Executing: sudo apt-get upgrade -y"'],
            ['sudo apt-get upgrade -y\n'],
            ['echo "Executing: sudo apt-get install python3 python3-pip python3-venv -y"'],
            ['sudo apt-get install python3 python3-pip python3-venv -y\n'],
            ['echo "Creating the venv..."'],
            [f'python3 -m venv ./{project_name}/venv\n'],
            ['echo "Activating the venv..."'],
            [f'source ./{project_name}/venv/bin/activate\n'],
            ['echo "Installing requirements..."'],
            [f'pip3 install -r ./{project_name}/requirements.txt']
        ]
    }
    for command in commands.get(project_type):
        script_content_join = "".join(command)
        script_content = script_content + script_content_join + "\n"

    return script_content
