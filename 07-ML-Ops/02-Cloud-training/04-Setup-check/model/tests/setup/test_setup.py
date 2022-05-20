
from tests.test_base import TestBase

import os
import pytest

from google.cloud import storage


TEST_ENV = os.getenv("TEST_ENV")


class TestGCPSetup(TestBase):

    def test_setup_cli_auth(self):
        """
        verify that `gcloud auth login` was successful
        """

        results = self.load_results()

        assert "No credentialed accounts." not in results, "the gcloud cli is not authorized to connect to any GCP account"

    @pytest.mark.skipif(TEST_ENV != "development", reason="only dev mode")
    def test_setup_key_env(self):
        """
        verify that `$GOOGLE_APPLICATION_CREDENTIALS` is defined
        """

        # verify env var presence
        assert os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), "GCP environment variable not defined"

    @pytest.mark.skipif(TEST_ENV != "development", reason="only dev mode")
    def test_setup_key_path(self):
        """
        verify that `$GOOGLE_APPLICATION_CREDENTIALS` points to an existing file
        """

        service_account_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        # verify env var path existence
        with open(service_account_key_path, "r") as file:
            content = file.read()

        assert content is not None

    @pytest.mark.skipif(TEST_ENV != "development", reason="only dev mode")
    def test_code_get_project(self):
        """
        retrieve default gcp project id with code
        """

        # get default project id
        client = storage.Client()
        project_id = client.project

        assert project_id is not None

    def test_setup_project_id(self):
        """
        verify that the provided project id is correct
        """

        makefile_project_id = self.load_results()
        real_project_id = self.load_results("test_setup_env_project_id")

        assert makefile_project_id == real_project_id

    def test_setup_bucket_exists(self):
        """
        verify that buckets exist
        """

        real_bucket_name = self.load_results("test_setup_env_bucket_name")

        assert len(real_bucket_name.split()) > 0, "no buckets found"

    def test_setup_bucket_name(self):
        """
        verify that the provided bucket name is correct
        """

        makefile_bucket_name = self.load_results()
        real_bucket_name = self.load_results("test_setup_env_bucket_name")

        assert makefile_bucket_name in real_bucket_name, "bucket does not exist"
        assert "/" not in makefile_bucket_name
        assert ":" not in makefile_bucket_name
