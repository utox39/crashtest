import argparse
import subprocess
from unittest.mock import patch

import pytest

import crash_test.error_codes
from crash_test.args_checker import instance_name_check, project_check, arguments_check
from crash_test.crashtest import CrashTest, args_parser
from crash_test.dependecies_checker import check_dependencies
from crash_test.error_logger import log_error
from crash_test.script_generator import script_generator


@pytest.fixture
def mock_multipass_command_execution():
    """
    Mocks the execution of multipass commands for testing purposes
    """
    with patch('subprocess.run') as mock_subprocess_run:
        yield mock_subprocess_run


class TestArgsCheck:
    def test_instance_name_check_valid(self):
        """
        Tests that when the instance name is valid the function returns True
        """
        assert instance_name_check("valid-instance-name") is True

    def test_instance_name_check_invalid(self):
        """
        Tests that when the instance name is invalid the function returns False
        """
        assert instance_name_check("invalid_instance_name") is False

    def test_project_check_valid(self, tmp_path):
        """
        Tests that when the project path is valid the function returns True
        """
        temp_test_project_folder = tmp_path / "test_project"
        temp_test_project_folder.mkdir()
        assert project_check(temp_test_project_folder) is True

    def test_project_check_non_existent_project_invalid(self):
        """
        Tests that when the project path does not exist the function returns False
        """
        assert project_check("non_existent_project") is False

    def test_project_check_is_file(self, tmp_path):
        temp_test_project_folder = tmp_path / "test_project"
        temp_test_project_folder.mkdir()

        with open(f"{temp_test_project_folder}/requirements.txt", "w") as file:
            file.write("test")

        assert project_check(f"{temp_test_project_folder}/requirements.txt") is False

    def test_project_check_returns_true(self, tmp_path):
        temp_test_project_folder = tmp_path / "test_project"
        temp_test_project_folder.mkdir()
        assert arguments_check(instance_name="valid-instance-name", project_path=temp_test_project_folder) is True

    def test_project_check_returns_false_with_invalid_instance_and_path(self):
        assert arguments_check(instance_name="invalid_instance_name", project_path="invalid/path") is False

    def test_project_check_returns_false_with_invalid_instance_and_valid_path(self, tmp_path):
        temp_test_project_folder = tmp_path / "test_project"
        temp_test_project_folder.mkdir()
        assert arguments_check(instance_name="invalid_instance_name", project_path=temp_test_project_folder) is False

    def test_project_check_returns_false_with_valid_instance_and_invalid_path(self):
        assert arguments_check(instance_name="valid-instance-name", project_path="invalid/path") is False


class TestScriptGenerator:
    def test_script_generator_returns_script_content(self):
        """
        Tests that script_generator() returns script content.
        """
        script_content = script_generator(project_name="test_project", project_type="python")
        assert script_content is not None

    def test_script_generator_returns_correct_script_content(self):
        """
        Tests that script_generator() generates correct script content.
        """
        test_project_name = "test_project"
        test_project_type = "python"
        script_content = script_generator(project_name=test_project_name, project_type=test_project_type)
        assert (test_project_name in script_content and test_project_type in script_content) is True


class TestDependencyCheck:
    def test_check_dependencies_returns_script_content(self, tmp_path):
        """
        Tests that check_dependencies() returns script content based on the project type.
        """
        tmp_project_path = tmp_path / "test_project"
        tmp_project_path.mkdir()

        with open(f"{tmp_project_path}/requirements.txt", "w") as file:
            file.write("test")

        script_content = check_dependencies(project_path=str(tmp_project_path))
        assert script_content is not None

    def test_check_dependencies_non_existent_path(self):
        assert check_dependencies(project_path="invalid/path") is None


class TestErrorLogger:
    def test_log_error_returns_error_message(self):
        """
        Tests that log_error() returns the correct error message based on the error code.
        """
        yellow = "\033[1m\033[33m"
        red = "\033[0;31m"
        # No colors
        nc = "\033[0m"

        error_codes = [crash_test.error_codes.NO_SUCH_FILE_OR_DIRECTORY_ERROR,
                       crash_test.error_codes.SINGLE_FILE_ERROR,
                       crash_test.error_codes.MULTIPASS_GENERIC_ERROR,
                       crash_test.error_codes.MULTIPASS_NOT_INSTALLED_ERROR,
                       crash_test.error_codes.INVALID_INSTANCE_NAME_ERROR,
                       crash_test.error_codes.NO_DEPENDENCIES_FOUND_ERROR,
                       crash_test.error_codes.NO_SUPPORTED_REQUIREMENTS_FILE_FOUND_ERROR
                       ]

        test_project_path = "test/path"

        for error in error_codes:
            match error:
                case crash_test.error_codes.NO_SUCH_FILE_OR_DIRECTORY_ERROR:
                    assert (log_error(
                        error_code=crash_test.error_codes.NO_SUCH_FILE_OR_DIRECTORY_ERROR,
                        project_path=test_project_path
                    ) == f"crashtest: error: cannot access {test_project_path}: No such file or directory.") is True
                case crash_test.error_codes.SINGLE_FILE_ERROR:
                    assert (log_error(
                        error_code=crash_test.error_codes.SINGLE_FILE_ERROR
                    ) == "Please only provide project directories. Single files are not allowed.") is True
                case crash_test.error_codes.MULTIPASS_GENERIC_ERROR:
                    assert (log_error(
                        error_code=crash_test.error_codes.MULTIPASS_GENERIC_ERROR
                    ) == f"{red}multipass: error: ") is True
                case crash_test.error_codes.MULTIPASS_NOT_INSTALLED_ERROR:
                    assert (log_error(
                        error_code=crash_test.error_codes.MULTIPASS_NOT_INSTALLED_ERROR
                    ) == "crashtest: error: Multipass is not installed!") is True
                case crash_test.error_codes.INVALID_INSTANCE_NAME_ERROR:
                    assert (log_error(
                        error_code=crash_test.error_codes.INVALID_INSTANCE_NAME_ERROR
                    ) == "crashtest: error: invalid instance name. The instance name should be like this: ") is True
                case crash_test.error_codes.NO_DEPENDENCIES_FOUND_ERROR:
                    assert (log_error(
                        error_code=crash_test.error_codes.NO_DEPENDENCIES_FOUND_ERROR
                    ) == f"{yellow}No dependencies detected.{nc}\n") is True
                case crash_test.error_codes.NO_SUPPORTED_REQUIREMENTS_FILE_FOUND_ERROR:
                    assert (log_error(
                        error_code=crash_test.error_codes.NO_SUPPORTED_REQUIREMENTS_FILE_FOUND_ERROR
                    ) == f"{yellow}No supported project requirements file was found!{nc}\n") is True


class TestCrashTest:
    def test_args_parser(self):
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
                instance_name='test_instance',
                project='test_project',
                delete=True,
                install_dependencies=True
        )):
            result = args_parser()

        assert result.instance_name == 'test_instance'
        assert result.project == 'test_project'
        assert result.delete is True
        assert result.install_dependencies is True

    def test_execute_multipass_command(self, mock_multipass_command_execution):
        """
        Tests that the mock was called exactly once and that that call was
        with the specified arguments
        :param mock_multipass_command_execution: function that mocks the execution of multipass commands
        """
        mock_multipass_command_execution.return_value.returncode = 0
        crashtest = CrashTest(None)
        crashtest.execute_multipass_command(["multipass", "launch", "--name", "test-instance"])
        mock_multipass_command_execution.assert_called_once_with(
            ["multipass", "launch", "--name", "test-instance"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
