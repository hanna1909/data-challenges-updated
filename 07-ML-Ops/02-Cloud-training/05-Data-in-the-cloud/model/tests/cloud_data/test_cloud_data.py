
from tests.test_base import TestBase

import os
import pytest

import numpy as np


TEST_ENV = os.getenv("TEST_ENV")


class TestCloudData(TestBase):

    def test_cloud_data_uploaded_blob(self):
        """
        verify that the training and validation csv are uploaded to the bucket
        """

        train_blob_stats = self.load_results()
        val_blob_stats = self.load_results("test_cloud_data_uploaded_blob_val")

        assert "No URLs matched" not in train_blob_stats, "cannot find uploaded training blob"
        assert "No URLs matched" not in val_blob_stats, "cannot find uploaded validation blob"

        training_content_length = [line for line in train_blob_stats.split("\n") if "Content-Length:" in line][0]
        training_content_length = training_content_length.strip().strip("Content-Length:").strip()

        assert int(training_content_length) == 1058666, "the uploaded file does not seem to be the correct size"

        validation_content_length = [line for line in val_blob_stats.split("\n") if "Content-Length:" in line][0]
        validation_content_length = validation_content_length.strip().strip("Content-Length:").strip()

        assert int(validation_content_length) == 1023391, "the uploaded file does not seem to be the correct size"

    def test_cloud_data_create_dataset(self):
        """
        verify that the bq dataset is created and the Makefile variable correct
        """

        dataset = self.load_results()
        source_datasets = self.load_results("test_cloud_data_create_dataset_source")

        assert self.is_content_line(dataset, source_datasets), "dataset does not exist"

    def test_cloud_data_create_table(self):
        """
        verify that the bq dataset tables are created and the Makefile variables correct
        """

        training_table = self.load_results("test_cloud_data_create_training_table")
        validation_table = self.load_results("test_cloud_data_create_validation_table")
        source_tables = self.load_results("test_cloud_data_create_table_source")

        assert training_table in source_tables, f"training table {training_table} does not exist"
        assert validation_table in source_tables, f"validation table {validation_table} does not exist"

    def test_cloud_data_table_content(self):
        """
        verify the format of the created bq tables
        """

        training_content = self.load_results("test_cloud_data_table_content_training")
        validation_table = self.load_results("test_cloud_data_table_content_validation")

        assert "|- key: timestamp" in training_content
        assert "|- fare_amount: float" in training_content
        assert "|- pickup_datetime: timestamp" in training_content
        assert "|- pickup_longitude: float" in training_content
        assert "|- pickup_latitude: float" in training_content
        assert "|- dropoff_longitude: float" in training_content
        assert "|- dropoff_latitude: float" in training_content
        assert "|- passenger_count: integer" in training_content

        assert "10000" in training_content
        assert "640000" in training_content

        assert "|- key: timestamp" in validation_table
        assert "|- fare_amount: float" in validation_table
        assert "|- pickup_datetime: timestamp" in validation_table
        assert "|- pickup_longitude: float" in validation_table
        assert "|- pickup_latitude: float" in validation_table
        assert "|- dropoff_longitude: float" in validation_table
        assert "|- dropoff_latitude: float" in validation_table
        assert "|- passenger_count: integer" in validation_table

        assert "10000" in validation_table
        assert "640000" in validation_table

    @pytest.mark.skipif(TEST_ENV != "development", reason="only dev mode")
    def test_cloud_data_bq_chunks(self):
        """
        verify the value of the `fare_amount` column for the first 10 observations of the training dataset table
        """

        from taxifare_model.data_sources.big_query import get_bq_chunk

        from taxifare_model.ml_logic.params import DATA_RAW_DTYPES_OPTIMIZED

        source = self.load_results()
        source = source.split("\n")[3:13]
        source = [float(s.strip("|").strip()) for s in source]
        source = [round(s, 1) for s in source]

        training_rows = get_bq_chunk("train_10k", 0, 10, DATA_RAW_DTYPES_OPTIMIZED)
        fare_amount = list(training_rows.fare_amount)
        fare_amount = [round(f, 1) for f in fare_amount]

        assert fare_amount == source

        # validate data types
        dtypes = training_rows.dtypes

        for column, data_type in DATA_RAW_DTYPES_OPTIMIZED.items():

            returned_data_type = dtypes[column]

            if data_type == "O":
                expected_data_type = object
            elif data_type == "float32":
                expected_data_type = np.float32
            elif data_type == "int8":
                expected_data_type = np.int8

            assert returned_data_type == expected_data_type, f"The column {column} is expected to contain the type {data_type}"
