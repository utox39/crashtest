#!/usr/bin/env python3

import argparse
import subprocess
from shutil import which
from sys import exit
from typing import Final, List

from colorama import Fore, Style

import crash_test.error_codes
from crash_test._version import __version__
from crash_test.args_checker import arguments_check
from crash_test.dependencies_checker import check_dependencies
from crash_test.error_logger import log_error
from crash_test.utils import get_scripts_absolute_path, check_script_path

SCRIPT_RELATIVE_PATH: Final[str] = "crash_test/scripts"


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
    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version=f"%(prog)s {__version__}")

    return parser.parse_args()


class CrashTest:
    def __init__(self, args):
        self.args = args

        if self.args:
            if self.args.project.endswith("/"):
                self.args.project = self.args.project[:-1]

            # The project name without the path
            self.project_name = self.args.project[self.args.project.rfind("/") + 1:]

    def run(self):
        self.create_instance()

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
            print(
                f"{log_error(error_code=crash_test.error_codes.MULTIPASS_GENERIC_ERROR)}{result.stderr}{Style.RESET_ALL}"
            )
            exit(result.returncode)

    def install_dependencies(self) -> None:
        """
        Create the installation script for the dependencies in the multipass instance and executes it.
        """
        if check_script_path(script_path=get_scripts_absolute_path(SCRIPT_RELATIVE_PATH)):
            script_path = check_dependencies(project_path=self.args.project,
                                             scripts_relative_path=SCRIPT_RELATIVE_PATH)

            if script_path:
                print(f"{Fore.GREEN}Installing dependencies...{Style.RESET_ALL}")

                transfer_script_command = ["multipass", "transfer", "-r", f"{script_path}",
                                           f"{self.args.instance_name}:./{self.project_name}"]

                self.execute_multipass_command(transfer_script_command)

                run_script_command = ["multipass", "exec", f"{self.args.instance_name}", "--", "bash",
                                      f"./{self.project_name}/python_dependencies.sh", f"{self.project_name}"]

                self.execute_multipass_command(run_script_command)
            else:
                print(log_error(error_code=crash_test.error_codes.NO_DEPENDENCIES_FOUND_ERROR))

    def create_instance(self) -> None:
        """
        Creates a Multipass instance and transfer the specified project to the newly created instance
        """
        if which("multipass") is not None:
            if arguments_check(instance_name=self.args.instance_name, project_path=self.args.project):
                # creates multipass session
                print(f"{Fore.GREEN}Creating multipass instance...\n{Style.RESET_ALL}")
                multipass_launch_command: List[str] = ["multipass", "launch", "--name", self.args.instance_name]
                self.execute_multipass_command(multipass_launch_command)
                print(f"{Fore.GREEN}Instance {self.args.instance_name} created successfully!\n{Style.RESET_ALL}")

                # transfers the specified project to the multipass session
                print(f"{Fore.GREEN}Transferring the project...\n{Style.RESET_ALL}")
                multipass_transfer_command: List[str] = ["multipass", "transfer", "-r", f"{self.args.project}/",
                                                         f"{self.args.instance_name}:."]
                self.execute_multipass_command(multipass_transfer_command)
                print(f"{Fore.GREEN}{self.project_name} transferred successfully!\n{Style.RESET_ALL}")

                # Install the dependencies
                if self.args.install_dependencies:
                    self.install_dependencies()

                # Opens a shell to the multipass instance
                print(f"{Fore.GREEN}Opening the shell...\n{Style.RESET_ALL}")
                multipass_shell_command: List[str] = ["multipass", "shell", self.args.instance_name]
                subprocess.run(multipass_shell_command)

                # Delete the instance if the --delete flag is specified
                if self.args.delete:
                    self.delete_instance()
        else:
            print(log_error(error_code=crash_test.error_codes.MULTIPASS_NOT_INSTALLED_ERROR))

    def delete_instance(self) -> None:
        """
        Delete the multipass instance if the -d --delete flag is specified
        """
        match input(
            "Are you sure you want to delete this instance? [Y/n]\n>>> "
        ).lower().strip()[0]:
            case "y":
                # Stops the instance
                print(f"\n{Fore.GREEN}Stopping the instance...{Style.RESET_ALL}")
                multipass_stop_command: List[str] = ["multipass", "stop", self.args.instance_name]
                self.execute_multipass_command(multipass_stop_command)
                print(f"{Fore.GREEN}Instance {self.args.instance_name} stopped.{Style.RESET_ALL}\n")

                # Deletes the instance
                print(f"{Fore.GREEN}Deleting the instance {self.args.instance_name}...{Style.RESET_ALL}\n")
                multipass_delete_command = ["multipass", "delete", self.args.instance_name]
                self.execute_multipass_command(multipass_delete_command)
                print(f"{Fore.GREEN}Instance deleted!{Style.RESET_ALL}")
            case _:
                print(f"{Fore.YELLOW}Elimination aborted.{Style.RESET_ALL}")


def main():
    crashtest: CrashTest = CrashTest(args=args_parser())
    crashtest.run()


if __name__ == '__main__':
    main()
