from unittest.mock import patch

from tests.test_base import TestBase

import numpy as np

# Override DATASET_SIZE just for this test to speed up results
@patch("taxifare.ml_logic.params.DATASET_SIZE", new="1k")
class TestInterface(TestBase):
    """Assert that code logic run and output the correct type.
    Do not check model performance
    """

    def test_preprocess_and_train_pass(self):

        from taxifare.interface.main_local import preprocess_and_train

        preprocess_and_train()

    def test_preprocess_and_train_value(self):

        results = self.load_results("test_preprocess_and_train", extension=".pickle")
        mae = results["metrics"]["val_mae"]

        assert isinstance(mae, float)

    def test_pred_pass(self):

        from taxifare.interface.main_local import pred

        pred()

    def test_pred_value(self):

        results = self.load_results("test_pred", extension=".pickle")
        y_pred = results["y_pred"].flat[0].tolist()

        assert isinstance(y_pred, float)

    def test_preprocess_pass(self):

        from taxifare.interface.main_local import preprocess

        preprocess(source_type="val")

    def test_preprocess_value(self):

        results = self.load_results("test_preprocess", extension=".pickle")
        data_processed_head = results["data_processed_head"]

        expected = np.array([[0.00000000e+00, 1.00000000e+00, 2.00000000e+00, 3.00000000e+00,
        4.00000000e+00, 5.00000000e+00, 6.00000000e+00, 7.00000000e+00,
        8.00000000e+00, 9.00000000e+00, 1.00000000e+01, 1.10000000e+01,
        1.20000000e+01, 1.30000000e+01, 1.40000000e+01, 1.50000000e+01,
        1.60000000e+01, 1.70000000e+01, 1.80000000e+01, 1.90000000e+01,
        2.00000000e+01, 2.10000000e+01, 2.20000000e+01, 2.30000000e+01,
        2.40000000e+01, 2.50000000e+01, 2.60000000e+01, 2.70000000e+01,
        2.80000000e+01, 2.90000000e+01, 3.00000000e+01, 3.10000000e+01,
        3.20000000e+01, 3.30000000e+01, 3.40000000e+01, 3.50000000e+01,
        3.60000000e+01, 3.70000000e+01, 3.80000000e+01, 3.90000000e+01,
        4.00000000e+01, 4.10000000e+01, 4.20000000e+01, 4.30000000e+01,
        4.40000000e+01, 4.50000000e+01, 4.60000000e+01, 4.70000000e+01,
        4.80000000e+01, 4.90000000e+01, 5.00000000e+01, 5.10000000e+01,
        5.20000000e+01, 5.30000000e+01, 5.40000000e+01, 5.50000000e+01,
        5.60000000e+01, 5.70000000e+01, 5.80000000e+01, 5.90000000e+01,
        6.00000000e+01, 6.10000000e+01, 6.20000000e+01, 6.30000000e+01,
        6.40000000e+01, 6.50000000e+01],
       [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 1.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00,
        0.00000000e+00, 9.65925813e-01, 2.58819044e-01, 1.53858485e-02,
        2.30518207e-02, 0.00000000e+00, 1.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 1.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 5.69999981e+00]])

        assert np.allclose(data_processed_head, expected, atol=1e-5)

    def test_train_pass(self):

        from taxifare.interface.main_local import train

        train()

    def test_train_value(self):

        results = self.load_results("test_train", extension=".pickle")
        metric = results['metrics']['mean_val']

        assert metric < 15
