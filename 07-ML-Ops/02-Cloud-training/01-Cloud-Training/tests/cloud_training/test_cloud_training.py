
from tests.test_base import TestBase


class TestCloudTraining(TestBase):

    def test_cloud_training_compute_api_enabled(self):
        """
        verify that the compute api is enabled
        """

        compute_api_status = self.load_results()

        assert "compute.googleapis.com" in compute_api_status, "compute api not enabled"
        assert "Compute Engine API" in compute_api_status, "compute api not enabled"

    def test_cloud_training_create_vm(self):
        """
        verify that the vm instance exists and the makefile variable is correct
        """

        instance_name = self.load_results()
        vm_list = self.load_results("test_cloud_training_create_vm_source")

        assert "not present in any resource" not in vm_list, "cannot find vm instance"
        assert instance_name in vm_list

    def test_cloud_training_operating_system(self):
        """
        verify that the vm os is ubuntu
        """

        operating_system = self.load_results()

        assert "Ubuntu" in operating_system

    def test_cloud_training_default_shell(self):
        """
        verify that the default vm shell is zsh
        """

        shell = self.load_results()

        assert "zsh" in shell

    def test_cloud_training_pyenv(self):
        """
        verify that pyenv is installed in the vm
        """

        pyenv_output = self.load_results()

        assert "Some useful pyenv commands are:" in pyenv_output

    def test_cloud_training_python_version(self):
        """
        verify that the lewagon virtual env is installed on python 3.8.12 in the vm
        """

        pyenv_versions_output = self.load_results()

        assert "3.8.12/envs/lewagon" in pyenv_versions_output
        assert "* lewagon" in pyenv_versions_output

    def test_cloud_training_list_projects(self):
        """
        verify that the vm code can list gcp projects
        """

        projects_list = self.load_results()
        project = self.load_results("test_cloud_training_project_id")

        assert project in projects_list
