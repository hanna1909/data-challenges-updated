from taxifare.ml_logic.params import (DATA_RAW_COLUMNS,
                                            DATA_RAW_DTYPES_OPTIMIZED,
                                            DATA_PROCESSED_DTYPES_OPTIMIZED)

from taxifare.data_sources.local_disk import (get_pandas_chunk,
                                                    save_local_chunk)

import os

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """

    # remove useless/redundant columns
    df = df.drop(columns=['key'])

    # remove buggy transactions
    df = df.drop_duplicates()  # TODO: handle in the data source if the data is consumed by chunks
    df = df.dropna(how='any', axis=0)
    df = df[(df.dropoff_latitude != 0) | (df.dropoff_longitude != 0) |
            (df.pickup_latitude != 0) | (df.pickup_longitude != 0)]
    df = df[df.passenger_count > 0]
    df = df[df.fare_amount > 0]

    # remove irrelevant/non-representative transactions (rows) for a training set
    df = df[df.fare_amount < 400]
    df = df[df.passenger_count < 8]
    df = df[df["pickup_latitude"].between(left=40.5, right=40.9)]
    df = df[df["dropoff_latitude"].between(left=40.5, right=40.9)]
    df = df[df["pickup_longitude"].between(left=-74.3, right=-73.7)]
    df = df[df["dropoff_longitude"].between(left=-74.3, right=-73.7)]

    print("\n✅ data cleaned")

    return df

def get_chunk(source_name: str,
              index: int = 0,
              chunk_size: int = None,
              verbose=False) -> pd.DataFrame:
    """
    return a chunk of the dataset between `index` and `index + chunk_size - 1`
    """

    if "processed" in source_name:
        columns = None
        dtypes = DATA_PROCESSED_DTYPES_OPTIMIZED
    else:
        columns = DATA_RAW_COLUMNS
        dtypes = DATA_RAW_DTYPES_OPTIMIZED

    chunk_df = get_pandas_chunk(path=source_name,
                                index=index,
                                chunk_size=chunk_size,
                                dtypes=dtypes,
                                columns=columns,
                                verbose=verbose)

    return chunk_df


def save_chunk(destination_name: str,
               is_first: bool,
               data: pd.DataFrame) -> None:
    """
    save chunk
    """

    save_local_chunk(path=destination_name,
                     data=data,
                     is_first=is_first)
