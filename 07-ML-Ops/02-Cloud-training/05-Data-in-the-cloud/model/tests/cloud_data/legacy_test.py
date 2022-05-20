
from taxifare_model.data_sources.big_query import get_bq_chunk, save_bq_chunk
from taxifare_model.ml_logic.preprocessor import preprocess_features

import pandas as pd


def __validate_get_bq_chunk():
    """
    should return a dataset containing the same data as the cli command:
        DATASET_SIZE=10k
        PROJECT=le-wagon-ds
        DATASET=taxifare_dataset
        TABLE=training
        bq query --nouse_legacy_sql "SELECT * from ${PROJECT}.${DATASET}.${TABLE}_${DATASET_SIZE} LIMIT 10 OFFSET 10"
    """

    from taxifare_model.ml_logic.params import DATA_RAW_DTYPES_OPTIMIZED

    df = get_bq_chunk(table="train_10k",
                      index=10,
                      chunk_size=10,
                      dtypes=DATA_RAW_DTYPES_OPTIMIZED)

    print(df)
    print(df.dtypes)

    return df


def __validate_save_bq_chunk():
    """
    should add chunk to the dataset table
    command to validate the added content:
        DATASET_SIZE=10k
        PROJECT=le-wagon-ds
        DATASET=taxifare_dataset
        TABLE=training_processed
        bq query --nouse_legacy_sql "SELECT * from ${PROJECT}.${DATASET}.${TABLE}_${DATASET_SIZE}"
    """

    df = __validate_get_bq_chunk()

    df_processed = pd.DataFrame(preprocess_features(df))

    save_bq_chunk(table="train_processed_10k", data=df_processed, is_first=True)
    save_bq_chunk(table="train_processed_10k", data=df_processed, is_first=False)


if __name__ == '__main__':

    # __validate_get_bq_chunk()
    __validate_save_bq_chunk()
