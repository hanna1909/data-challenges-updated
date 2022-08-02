"""
taxifare model package params
load and validate the environment variables in the `.env`
"""

import os

import numpy as np

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
