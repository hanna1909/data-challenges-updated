
from tests.test_base import TestBase


class TestCloudPrediction(TestBase):

    def test_cloud_prediction_pred(self):
        """
        verify the prediction
        """

        prediction = self.load_results("pred")

        assert prediction is not None
