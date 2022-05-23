
from tests.test_base import TestBase

import re


class TestPrefect(TestBase):

    def test_prefect_parameters(self):
        """
        verify that the prefect parameters are correctly set
        """

        flow_name = self.load_results("test_prefect_flow_name")
        backend = self.load_results("test_prefect_backend")
        log_level = self.load_results("test_prefect_log_level")

        assert flow_name is not None
        assert backend == "local"
        assert log_level is not None
