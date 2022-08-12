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

    def test_preprocess_and_train_last_run_value(self):

        results = self.load_results("test_preprocess_and_train", extension=".pickle")
        mae = results["metrics"]["mae"]

        assert isinstance(mae, float), "last time you ran this preprocess_and_train(), it didn't store any mae as float"

    def test_pred_pass(self):

        from taxifare.interface.main_local import pred

        pred()

    def test_pred_last_run_value(self):

        results = self.load_results("test_pred", extension=".pickle")
        y_pred = results["y_pred"].flat[0].tolist()

        assert isinstance(y_pred, float), "Last time you ran pred(), it didn't store any predictions as float"

    def test_preprocess_pass(self):

        from taxifare.interface.main_local import preprocess

        preprocess(source_type="val")

    def test_preprocess_last_run_value(self):

        results = self.load_results("test_preprocess", extension=".pickle")
        data_processed_head = results["data_processed_head"]

        assert data_processed_head.shape[1] == 66, "Last time you ran preprocess(), it output the wrong number of columns after preprocessing. Should be 66 (65 feature + 1 target)"

    def test_train_pass(self):

        from taxifare.interface.main_local import train

        train()
