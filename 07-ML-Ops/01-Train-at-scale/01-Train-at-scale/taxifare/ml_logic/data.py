from taxifare.ml_logic.params import (DATA_RAW_COLUMNS,
                                            DATA_RAW_DTYPES_OPTIMIZED,
                                            DATA_PROCESSED_DTYPES_OPTIMIZED)

import os

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """

    # remove useless/redundant columns
    # YOUR CODE HERE

    # remove buggy transactions
    # YOUR CODE HERE

    # remove irrelevant/non-representative transactions (rows) for a training set
    # YOUR CODE HERE

    print("\n✅ data cleaned")

    return df
