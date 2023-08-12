#!/usr/bin/env python3

import argparse
import subprocess


class CrashTest:

    def __init__(self, args):
        self.args = args

    def run(self):
        self.create_multipass_session()

    def create_multipass_session(self):
        print("Creating multipass instance...\n")
        # creates multipass session
        subprocess.run(["multipass", "launch", "--name", self.args.instance_name])
        print(f"Instance {self.args.instance_name} created successfully\n")

        print("Transferring the project...\n")
        # transfers the project to be tested to the multipass session
        subprocess.run(["multipass", "transfer", "-r", f"{self.args.project}/", f"{self.args.instance_name}:."])
        print(f"Project {self.args.project} transferred successfully\n")

        print("Opening the shell...\n")
        subprocess.run(["multipass", "shell", self.args.instance_name])

        if self.args.delete:
            match input("Are you sure you want to delete this instance? [Y/n]\n>>> ").lower().strip():
                case "y":
                    print(f"\nDeleting the instance {self.args.instance_name}\n")
                    subprocess.run(["multipass", "stop", self.args.instance_name])
                    subprocess.run(["multipass", "delete", self.args.instance_name])
                    print("Deleted")
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
                        help="Project folder to transfer to the multipass instance to be tested"
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
