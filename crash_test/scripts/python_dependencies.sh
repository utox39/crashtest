#!/usr/bin/env bash

#######################################################################################
# Description:
# This script updates the multipass instance; installs python3, pip3 and python3 venv;
# deletes any existing venv and creates a new one; installs all the dependencies from
# requirements.txt
#######################################################################################


PROJECT_NAME=$1

printf "\nExecuting: sudo apt-get update\n"
sudo apt-get update

printf "\nExecuting: sudo apt-get upgrade -y\n"
sudo apt-get upgrade -y

# Install python3, pip3 and python3 venv
printf "\nExecuting: sudo apt-get install python3 python3-pip python3-venv -y\n"
sudo apt-get install python3 python3-pip python3-venv -y

# Check if a venv already exists then deletes it
if [ -d ./"$PROJECT_NAME"/ ]; then
  rm -r ./"$PROJECT_NAME"/venv
fi

# Create a new python venv
printf "\nCreating the venv...\n"
python3 -m venv ./"$PROJECT_NAME"/venv

# Activate the python venv
printf "\nActivating the venv...\n"
# shellcheck disable=SC1090
source ./"$PROJECT_NAME"/venv/bin/activate

# Install all the dependencies from requirements.txt
printf "\nInstalling requirements...\n"
pip3 install -r ./"$PROJECT_NAME"/requirements.txt