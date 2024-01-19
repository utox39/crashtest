#!/usr/bin/env bash

###############################################################################
# Description:
# This script updates the multipass instance, installs nvm and the latest version
# of node and npm
###############################################################################

printf "\nExecuting: sudo apt-get update\n"
sudo apt-get update

printf "\nExecuting: sudo apt-get upgrade -y\n"
sudo apt-get upgrade -y

# Install nvm
printf "\nInstalling Node and Npm via nvm\n"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Install node lts and the latest version of npm
nvm install --lts --latest-npm node

npm install