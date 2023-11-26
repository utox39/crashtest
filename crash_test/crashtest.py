#!/usr/bin/env python3

import argparse
import subprocess

from shutil import which
from sys import exit
from typing import Final, List

from utils.args_check import arguments_check
from utils.dependecies_check import check_dependencies

GREEN: Final[str] = "\033[1;32m"
YELLOW: Final[str] = "\033[1m\033[33m"
BLUE: Final[str] = "\033[1m\033[34m"
RED: Final[str] = "\033[0;31m"
# No colors
NC: Final[str] = "\033[0m"


def args_parser():
    parser = argparse.ArgumentParser(
        description="Create a multipass instance to test your dAnGeRoUs project",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-i",
                        "--instance-name",
                        type=str,
                        required=True,
                        help="Multipass instance name"
                        )
    parser.add_argument("-p",
                        "--project",
                        type=str,
                        required=True,
                        help="Project folder to transfer to the multipass instance to be tested"
                        )
    parser.add_argument("-d",
                        "--delete",
                        action="store_true",
                        help="Delete the instance"
                        )
    parser.add_argument("--install-dependencies",
                        action="store_true",
                        help="Installs the dependencies for the project"
                        )

    return parser.parse_args()


class CrashTest:

    def __init__(self, args):
        self.args = args

        if self.args.project.endswith("/"):
            self.args.project = self.args.project[:-1]

        # The project name without the path
        self.project_name = self.args.project[self.args.project.rfind("/") + 1:]

    def run(self):
        self.create_test_instance()

    @staticmethod
    def execute_multipass_command(command) -> None:
        """
        Executes a specified multipass command and prints possible errors
        :param command: the Multipass command to execute
        """
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.stdout:
            print(f"Output: {result.stdout}")

        if result.returncode != 0:
            print(f"{RED}multipass: error: {result.stderr}{NC}")
            exit(result.returncode)

    def install_dependencies(self) -> None:
        """
        Create the installation script for the dependencies in the multipass instance and executes it.
        """
        script_content = check_dependencies(self.args.project)

        if script_content:
            print(f"{GREEN}Installing dependencies...{NC}")

            create_script_command = ["multipass", "exec", f"{self.args.instance_name}", "--", "sh", "-c",
                                     f'echo "{script_content}" > ./{self.project_name}/python_dependencies.sh']

            self.execute_multipass_command(create_script_command)

            run_script_command = ["multipass", "exec", f"{self.args.instance_name}", "--", "bash",
                                  f"./{self.project_name}/python_dependencies.sh"]

            self.execute_multipass_command(run_script_command)
        else:
            print(f"{YELLOW}No dependencies detected.{NC}\n")

    def create_test_instance(self) -> None:
        """
        Creates a Multipass instance and transfer the specified project to the newly created instance
        """
        if which("multipass") is not None:
            if arguments_check(instance_name=self.args.instance_name, project_path=self.args.project):
                # creates multipass session
                print(f"{GREEN}Creating multipass instance...\n{NC}")
                multipass_launch_command: List[str] = ["multipass", "launch", "--name", self.args.instance_name]
                self.execute_multipass_command(multipass_launch_command)
                print(f"{GREEN}Instance {self.args.instance_name} created successfully!\n{NC}")

                # transfers the specified project to the multipass session
                print(f"{GREEN}Transferring the project...\n{NC}")
                multipass_transfer_command: List[str] = ["multipass", "transfer", "-r", f"{self.args.project}/",
                                                         f"{self.args.instance_name}:."]
                self.execute_multipass_command(multipass_transfer_command)
                print(f"{GREEN}{self.project_name} transferred successfully!\n{NC}")

                # Install the dependencies
                if self.args.install_dependencies:
                    self.install_dependencies()

                # Opens a shell to the multipass instance
                print(f"{GREEN}Opening the shell...\n{NC}")
                multipass_shell_command: List[str] = ["multipass", "shell", self.args.instance_name]
                subprocess.run(multipass_shell_command)

                # Delete the instance if the --delete flag is specified
                if self.args.delete:
                    self.delete_instance()
        else:
            print("Crashtest: error: Multipass is not installed!")

    def delete_instance(self) -> None:
        """
        Delete the multipass instance if the -d --delete flag is specified
        """
        match input(
            f"{BLUE}Are you sure you want to delete this instance? [{GREEN}Y{BLUE}/{RED}n{BLUE}]\n>>> {NC}"
        ).lower().strip():
            case "y":
                # Stops the instance
                print(f"\n{GREEN}Stopping the instance...{NC}\n")
                multipass_stop_command: List[str] = ["multipass", "stop", self.args.instance_name]
                self.execute_multipass_command(multipass_stop_command)
                print(f"{GREEN}Instance {self.args.instance_name} stopped.{NC}\n")

                # Deletes the instance
                print(f"{GREEN}Deleting the instance {self.args.instance_name}...{NC}\n")
                multipass_delete_command = ["multipass", "delete", self.args.instance_name]
                self.execute_multipass_command(multipass_delete_command)
                print(f"{GREEN}Instance deleted!{NC}")
            case _:
                print(f"{YELLOW}Elimination aborted.{NC}")


def main():
    crash_test: CrashTest = CrashTest(args=args_parser())
    crash_test.run()


if __name__ == '__main__':
    main()
