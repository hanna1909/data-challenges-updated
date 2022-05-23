
from tests.test_base import TestBase


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

    def test_prefect_flow(self):
        """
        test complete workflow lifecycle
        """

        flow = self.load_results()

        assert "Flow run SUCCESS: all reference tasks succeeded" in flow


def write_prefect_flow():

    from taxifare_flow.flow import build_flow

    import os

    flow = build_flow()

    mlflow_experiment = os.environ.get("MLFLOW_EXPERIMENT")

    flow.run(parameters=dict(
        experiment=mlflow_experiment))
