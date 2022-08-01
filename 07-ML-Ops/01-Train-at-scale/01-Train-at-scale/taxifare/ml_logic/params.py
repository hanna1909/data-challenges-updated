"""
taxifare model package params
load and validate the environment variables in the `.env`
"""

import os

import numpy as np

DATASET_SIZE = "10k"             # ["1k","10k", "100k", "500k"]
VALIDATION_DATASET_SIZE = "10k"  # ["1k", "10k", "100k", "500k"]
CHUNK_SIZE = 2000               # ["200", "2000", "20000", "100000", "1000000"]
LOCAL_DATA_PATH = os.path.join(os.getenv('HOME'), ".lewagon", "mlops", "data")
LOCAL_REGISTRY_PATH =  os.path.join(os.getenv('HOME'), ".lewagon", "mlops", "training_outputs")

DATA_RAW_DTYPES_OPTIMIZED = {
    "key": "O",
    "fare_amount": "float32",
    "pickup_datetime": "O",
    "pickup_longitude": "float32",
    "pickup_latitude": "float32",
    "dropoff_longitude": "float32",
    "dropoff_latitude": "float32",
    "passenger_count": "int8"
}
DATA_RAW_COLUMNS = DATA_RAW_DTYPES_OPTIMIZED.keys()

DATA_PROCESSED_DTYPES_OPTIMIZED = np.float32
