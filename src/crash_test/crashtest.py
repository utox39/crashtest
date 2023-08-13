#!/usr/bin/env python3

import argparse
import os
import subprocess

from shutil import which
from sys import exit


class CrashTest:

    def __init__(self, args):
        self.args = args

    def run(self):
        self.create_test_instance()
        if self.args.delete:
            self.delete_instance()

    def args_check(self) -> bool:
        """
        Checks the instance name format and if the specified project exists
        :return: bool: True if the checks pass, False if the check fails.
        """
        instance_name_check = False
        project_check = False

        if "_" in self.args.instance_name:
            instance_name: str = self.args.instance_name
            correct_format: str = instance_name.replace("_", "-")
            print(f"Crashtest: error: invalid instance name. The instance name should be like this: {correct_format}")
        else:
            instance_name_check = True

        if os.path.exists(self.args.project):
            project_check = True
        else:
            print(f"Crashtest: error: cannot access {self.args.project}: No such file or directory")

        if instance_name_check and project_check:
            return True
        else:
            return False

    @staticmethod
    def execute_multipass_command(command) -> None:
        """
        Executes a specified multipass command and prints possible errors
        :param command: the Multipass command to execute
        """
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Multipass: error: {result.stderr}")
            exit(result.returncode)

    def create_test_instance(self) -> None:
        """
        Creates a Multipass instance and transfer the specified project to the newly created instance
        """
        if which("multipass") is not None:
            if self.args_check():
                # TODO: migliorare l'output
                print("Creating multipass instance...\n")
                # creates multipass session
                multipass_launch_command = ["multipass", "launch", "--name", self.args.instance_name]
                self.execute_multipass_command(multipass_launch_command)
                print(f"Instance {self.args.instance_name} created successfully!\n")

                print("Transferring the project...\n")
                # transfers the specified project to the multipass session
                multipass_transfer_command = ["multipass", "transfer", "-r", f"{self.args.project}/",
                                              f"{self.args.instance_name}:."]
                self.execute_multipass_command(multipass_transfer_command)
                print(f"{self.args.project} transferred successfully!\n")

                print("Opening the shell...\n")
                multipass_shell_command = ["multipass", "shell", self.args.instance_name]
                subprocess.run(multipass_shell_command)
        else:
            print("Crashtest: error: Multipass is not installed!")

    def delete_instance(self) -> None:
        """
        Delete the multipass instance if the -d --delete flag is specified
        """
        match input("Are you sure you want to delete this instance? [Y/n]\n>>> ").lower().strip():
            case "y":
                # Stops the instance
                print("\nStopping the instance...\n")
                multipass_stop_command = ["multipass", "stop", self.args.instance_name]
                self.execute_multipass_command(multipass_stop_command)
                print(f"Instance {self.args.instance_name} stopped\n")

                # Deletes the instance
                print(f"Deleting the instance {self.args.instance_name}...\n")
                multipass_delete_command = ["multipass", "delete", self.args.instance_name]
                self.execute_multipass_command(multipass_delete_command)
                print("Instance deleted!")
            case _:
                print("Elimination aborted")


def main():
    parser = argparse.ArgumentParser(
        description="Create a multipass instance to test your dAnGeRoUs project",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-i",
                        "--instance-name",
                        type=str,
                        help="Multipass instance name"
                        )
    parser.add_argument("-p",
                        "--project",
                        type=str,
                        help="Project file/folder to transfer to the multipass instance to be tested"
                        )
    parser.add_argument("-d",
                        "--delete",
                        action="store_true",
                        help="Delete the instance"
                        )

    args = parser.parse_args()

    crash_test: CrashTest = CrashTest(args=args)
    crash_test.run()


if __name__ == '__main__':
    main()
