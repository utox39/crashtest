#!/usr/bin/env bash

PROJECT_NAME=$1

printf "\nExecuting: sudo apt-get update\n"
sudo apt-get update

printf "\nExecuting: sudo apt-get upgrade -y\n"
sudo apt-get upgrade -y

printf "\nExecuting: sudo apt-get install python3 python3-pip python3-venv -y\n"
sudo apt-get install python3 python3-pip python3-venv -y

# Check if venv already exists then deletes it
if [ -d ./"$PROJECT_NAME"/ ]; then
  rm -r ./"$PROJECT_NAME"/venv
fi

printf "\nCreating the venv...\n"
python3 -m venv ./"$PROJECT_NAME"/venv

printf "\nActivating the venv...\n"
# shellcheck disable=SC1090
source ./"$PROJECT_NAME"/venv/bin/activate

printf "\nInstalling requirements...\n"
pip3 install -r ./"$PROJECT_NAME"/requirements.txt