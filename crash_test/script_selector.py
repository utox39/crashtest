#!/usr/bin/env python3

from typing import Final


# TODO: 3 implementare la scelta dello script (Attenzione: la cartella degli script si troverà nel site package)
# TODO: 2 Add support for npm

def script_generator(project_name: str, project_type: str) -> str:
    script_content = ""
    commands: Final[dict] = {
        "python": [
            ['#!/usr/bin/env bash\n'],
            ['printf "\nExecuting: sudo apt-get update\n"'],
            ['sudo apt-get update\n'],
            ['printf "\nExecuting: sudo apt-get upgrade -y\n"'],
            ['sudo apt-get upgrade -y\n'],
            ['printf "\nExecuting: sudo apt-get install python3 python3-pip python3-venv -y\n"'],
            ['sudo apt-get install python3 python3-pip python3-venv -y\n'],
            ['printf "\nCreating the venv...\n"'],
            [f'python3 -m venv ./{project_name}/venv\n'],
            ['printf "\nActivating the venv...\n"'],
            [f'source ./{project_name}/venv/bin/activate\n'],
            ['printf "\nInstalling requirements...\n"'],
            [f'pip3 install -r ./{project_name}/requirements.txt']
        ]
    }
    for command in commands.get(project_type):
        script_content_join = "".join(command)
        script_content = script_content + script_content_join + "\n"

    return script_content
