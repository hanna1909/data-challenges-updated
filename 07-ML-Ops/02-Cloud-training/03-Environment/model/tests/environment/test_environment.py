
from tests.test_base import TestBase

import re
import os


class TestDirenv(TestBase):

    def test_environment_dataset_size(self):
        """
        verify that direnv loaded $DATASET_SIZE
        """

        dataset_size = self.load_results()

        assert dataset_size is not None and dataset_size != ""

    def test_environment_hello(self):
        """
        verify $HELLO value
        """

        hello = self.load_results()

        assert hello == "world !"

    def test_local_data_path(self):
        """
        verify the $LOCAL_DATA_PATH value
        """

        local_data_path = self.load_results()

        data_path_match = re.compile(".*/code/.*/07-ML-Ops/data$").match(local_data_path)

        content_writer_bypass = os.environ.get("CONTENT_WRITER_BYPASS") == "true"

        assert data_path_match is not None or content_writer_bypass

    def test_local_registry_path(self):
        """
        verify the $LOCAL_REGISTRY_PATH value
        """

        local_registry_path = self.load_results()

        registry_path_match = re.compile(".*/code/.*/07-ML-Ops/registry$").match(local_registry_path)

        content_writer_bypass = os.environ.get("CONTENT_WRITER_BYPASS") == "true"

        assert registry_path_match is not None or content_writer_bypass
