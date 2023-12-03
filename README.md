# Crashtest

[![codecov](https://codecov.io/gh/utox39/crashtest/graph/badge.svg?token=WH50XIU1V9)](https://codecov.io/gh/utox39/crashtest)
[<img alt="PyPI - Version" src="https://img.shields.io/pypi/v/crash-test-multipass">
](https://pypi.org/project/crash-test-multipass/)
[<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/crash-test-multipass">
](https://pypistats.org/packages/crash-test-multipass)
[<img alt="GitHub Workflow Status (with event)" src="https://img.shields.io/github/actions/workflow/status/utox39/crashtest/.github%2Fworkflows%2Ftest-package.yml">
](https://github.com/utox39/crashtest/actions)
---

- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Description

Crashtest is a command-line tool to create a [Multipass](https://multipass.run/) instance and transfer a project to test
to the newly created instance.

## Requirements

- Python 3
- [Multipass](https://multipass.run/)

## Installation

```console
$ pip3 install --upgrade crash-test-multipass
```

NOTE: After installing crash-test-multipass with pip if you have not added ~/.local/bin (macOS/Linux) to $PATH you will
be asked to do so with a warning that should look like this:

```console
WARNING: The script crash-test-multipass is installed in '/home/ubuntu/.local/bin' which is not on PATH.
Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

## Usage

#### Create a new instance and transfer a project

```console
$ crashtest --instance-name INSTANCE_NAME --project PROJECT
```

#### Create a new instance, transfer a project and install the dependencies

NOTE: Currently only requirements.txt (python) is supported

```console
$ crashtest --instance-name INSTANCE_NAME --project PROJECT --install-dependencies
```

#### Delete the instance after finishing to test

```console
$ crashtest --instance-name INSTANCE_NAME --project PROJECT --delete
```

## Contributing

If you would like to contribute to this project just create a pull request which I will try to review as soon as
possible.
