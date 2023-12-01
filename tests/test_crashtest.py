import pytest
import subprocess

from unittest.mock import patch

from crash_test.crashtest import CrashTest
from crash_test.args_checker import instance_name_check, project_check
from crash_test.script_generator import script_generator
from crash_test.dependecies_checker import check_dependencies


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
        project_folder = tmp_path / "test_project"
        project_folder.mkdir()
        assert project_check(project_folder) is True

    def test_project_check_non_existent_project_invalid(self):
        """
        Tests that when the project path does not exist the function returns False
        """
        assert project_check("non_existent_project") is False


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
            file.write("colorama>=0.4.6")

        script_content = check_dependencies(project_path=str(tmp_project_path))
        assert script_content is not None


class TestCrashTest:
    def test_execute_multipass_command(self, mock_multipass_command_execution):
        """
        Tests that the mock was called exactly once and that that call was
        with the specified arguments
        :param mock_multipass_command_execution: function that mocks the execution of multipass commands
        """
        mock_multipass_command_execution.return_value.returncode = 0
        crash_test = CrashTest(None)
        crash_test.execute_multipass_command(["multipass", "launch", "--name", "test-instance"])
        mock_multipass_command_execution.assert_called_once_with(
            ["multipass", "launch", "--name", "test-instance"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
