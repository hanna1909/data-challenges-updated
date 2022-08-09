from tests.test_base import write_result

from taxifare.ml_logic.data import clean_data

from taxifare.ml_logic.params import (CHUNK_SIZE,
                                            DATA_RAW_DTYPES_OPTIMIZED,
                                            DATA_PROCESSED_DTYPES_OPTIMIZED,
                                            DATA_RAW_COLUMNS,
                                            DATASET_SIZE,
                                            VALIDATION_DATASET_SIZE,
                                            LOCAL_DATA_PATH)

from taxifare.ml_logic.preprocessor import preprocess_features

from taxifare.ml_logic.model import (initialize_model,
                                           compile_model,
                                           train_model)

from taxifare.ml_logic.registry import (save_model,
                                              load_model)

import numpy as np
import pandas as pd
import os


def preprocess_and_train():
    """
    Load historical data in memory, clean and preprocess it, train a Keras model on it,
    save the model, and finally compute & save a performance metric
    on a validation set holdout at the `model.fit()` level
    """

    print("\n⭐️ use case: preprocess and train basic")


    # Retrieve raw data
    data_raw_path = os.path.join(LOCAL_DATA_PATH, "raw", f"train_{DATASET_SIZE}.csv")
    data = pd.read_csv(data_raw_path, dtype=DATA_RAW_DTYPES_OPTIMIZED)

    # Clean data using ml_logic.data.clean_data
    data_cleaned = clean_data(data)

    # Create X, y
    X = data_cleaned.drop("fare_amount", axis=1)
    y = data_cleaned[["fare_amount"]]

    # Preprocess X using `preprocessor.py`
    X_processed = preprocess_features(X)

    # Train model on X_processed and y, using `model.py`
    model = None
    learning_rate = 0.001
    batch_size = 64
    model = initialize_model(X_processed)
    model = compile_model(model, learning_rate)
    model, history = train_model(model, X_processed, y, batch_size, validation_split=0.3)

    # Compute the validation metric (min val mae of the holdout set)
    metrics = dict(val_mae=None)
    metrics = dict(val_mae=np.min(history.history['val_mae']))

    # Save trained model
    params = dict(
        learning_rate=learning_rate,
        batch_size=batch_size)
    save_model(model, params=params, metrics=metrics)

    # 🧪 Write test output (used by Kitt to track progress - do not remove)
    write_result(name="test_preprocess_and_train", subdir="train_at_scale", metrics=metrics)

    print("✅ preprocess_and_train() done")

def preprocess(training_set=True):
    """
    Preprocess the dataset iteratively, loading data by chunks fitting in memory,
    processing each chunk, appending each of them to a final dataset preprocessed,
    and saving final prepocessed dataset as CSV
    """

    print("\n⭐️ use case: preprocess")

    # local saving paths given to you (do not overwrite these data_path variable)
    if training_set:
        source_name = f"train_{DATASET_SIZE}.csv"
        destination_name = f"train_processed_{DATASET_SIZE}.csv"
    else:
        source_name = f"val_{VALIDATION_DATASET_SIZE}.csv"
        destination_name = f"val_processed_{VALIDATION_DATASET_SIZE}.csv"

    data_raw_path = os.path.abspath(os.path.join(
        LOCAL_DATA_PATH, "raw", source_name))
    data_processed_path = os.path.abspath(os.path.join(
        LOCAL_DATA_PATH, "processed", destination_name))

    # iterate on the dataset, by chunks
    chunk_id = 0

    while (True):
        print(f"processing chunk n°{chunk_id}...")

        # load in memory the chunk numbered `chunk_id` of size CHUNK_SIZE
        # 🎯 Hint: check out pd.read_csv(skiprows=..., nrows=...)


        one_if_first_chunk = 1 if chunk_id == 0 else 0

        try:
            data_raw_chunk = pd.read_csv(
                    data_raw_path,
                    header=None, # ignore headers
                    skiprows=(chunk_id * CHUNK_SIZE) + one_if_first_chunk, # first chunk has headers
                    nrows=CHUNK_SIZE,
                    dtype=DATA_RAW_DTYPES_OPTIMIZED,
                    )

            data_raw_chunk.columns = DATA_RAW_COLUMNS

        except pd.errors.EmptyDataError:
            data_raw_chunk = None  # end of data

        # Break out of while loop if data is none
        if data_raw_chunk is None:
            break

        # clean chunk
        data_clean_chunk = clean_data(data_raw_chunk)
        # Break out of while loop if cleaning removed all rows
        if len(data_clean_chunk) ==0:
            break

        # create X_chunk,y_chunk
        X_chunk = data_clean_chunk.drop("fare_amount", axis=1)
        y_chunk = data_clean_chunk[["fare_amount"]]

        # create X_processed_chunk and concatenate (X_processed_chunk, y_chunk) into data_processed_chunk
        X_processed_chunk = preprocess_features(X_chunk)
        data_processed_chunk = pd.DataFrame(
            np.concatenate((X_processed_chunk, y_chunk), axis=1))

        # Save the chunk of the dataset to local disk (append to existing csv to build it chunk by chunk)
        # 🎯 Hints1: check out pd.to_csv(mode=...)
        data_processed_chunk.to_csv(data_processed_path,
                mode="w" if chunk_id==0 else "a",
                header=chunk_id==0,
                index=False)

        chunk_id += 1

    # 🧪 Write test output (used by Kitt to track progress - do not remove)
    if training_set:
        data_processed = pd.read_csv(data_processed_path, header=None, dtype=DATA_PROCESSED_DTYPES_OPTIMIZED).to_numpy()
        write_result(name="test_preprocess", subdir="train_at_scale",
                    data_processed_head=data_processed[0:2])

    print("✅ data processed saved entirely")


def train():
    """
    Training on the full (already preprocessed) dataset, by loading it
    chunk-by-chunk, and updating the weight of the model for each chunks.
    Save model, compute validation metrics on a holdout validation set that is
    common to all chunks.
    """
    print("\n ⭐️ use case: train")

    # Validation Set: Load a validation set common to all chunks and create X_val, y_val
    data_val_processed_path = os.path.abspath(os.path.join(
        LOCAL_DATA_PATH, "processed", f"val_processed_{VALIDATION_DATASET_SIZE}.csv"))

    data_val_processed = pd.read_csv(
        data_val_processed_path,
        header=None,
        dtype=DATA_PROCESSED_DTYPES_OPTIMIZED
        ).to_numpy()

    X_val = data_val_processed[:, :-1]
    y_val = data_val_processed[:, -1]

    # Iterate on the full training dataset chunk per chunks.
    # Break out of the loop if you receive no more data to train upon!
    model = None
    chunk_id = 0
    metrics_val_list = []  # store each metrics_val_chunk

    while (True):
        print(f"loading and training on preprocessed chunk n°{chunk_id}...")

        # Load chunk of preprocess data and create (X_train_chunk, y_train_chunk)
        path = os.path.abspath(os.path.join(
            LOCAL_DATA_PATH, "processed", f"train_processed_{DATASET_SIZE}.csv"))

        try:
            data_processed_chunk = pd.read_csv(
                    path,
                    header=None,
                    skiprows=(chunk_id * CHUNK_SIZE),
                    nrows=CHUNK_SIZE,
                    dtype=DATA_PROCESSED_DTYPES_OPTIMIZED,
                    ).to_numpy()

        except pd.errors.EmptyDataError:
            data_processed_chunk = None  # end of data

        # Break out of while loop if we have no data to train upon
        if data_processed_chunk is None:
            break

        X_train_chunk = data_processed_chunk[:, :-1]
        y_train_chunk = data_processed_chunk[:, -1]

        # Train a model incrementally and print validation metrics for this chunk
        learning_rate = 0.001
        batch_size = 64
        if model is None:
            model = initialize_model(X_train_chunk)
            model = compile_model(model, learning_rate)

        model, history = train_model(model,
                                     X_train_chunk,
                                     y_train_chunk,
                                     batch_size,
                                     validation_data=(X_val, y_val))
        metrics_val_chunk = np.min(history.history['val_mae'])
        metrics_val_list.append(metrics_val_chunk)
        print(metrics_val_chunk)

        chunk_id += 1

    # Save model and training params
    params = dict(
        learning_rate=learning_rate,
        batch_size=batch_size,
        incremental=True,
        chunk_size=CHUNK_SIZE)

    metrics_val_mean_all_chunks = np.mean(np.array(metrics_val_list))
    metrics = dict(mean_val=metrics_val_mean_all_chunks)

    save_model(model, params=params, metrics=metrics)

    # 🧪 Write test output (used by Kitt to track progress - do not remove)
    write_result(name="test_train", subdir="train_at_scale",
                 metrics=metrics)

    print("✅ model trained and saved")


def pred(X_pred: pd.DataFrame = None) -> np.ndarray:

    if X_pred is None:

        X_pred = pd.DataFrame(dict(
            key=["2013-07-06 17:18:00"],  # useless but the pipeline requires it
            pickup_datetime=["2013-07-06 17:18:00 UTC"],
            pickup_longitude=[-73.950655],
            pickup_latitude=[40.783282],
            dropoff_longitude=[-73.984365],
            dropoff_latitude=[40.769802],
            passenger_count=[1]))

    model = load_model()

    # preprocess the new data
    X_processed = preprocess_features(X_pred)

    # make a prediction
    y_pred = model.predict(X_processed)

    # 🧪 Write test output (used by Kitt to track progress - do not remove)
    write_result(name="test_pred", subdir="train_at_scale", y_pred=y_pred)
    print("✅ prediction done: ", y_pred, y_pred.shape)

    return y_pred


if __name__ == '__main__':
    try:
        preprocess_and_train()
        pred()
    except:
        import ipdb, traceback, sys
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)