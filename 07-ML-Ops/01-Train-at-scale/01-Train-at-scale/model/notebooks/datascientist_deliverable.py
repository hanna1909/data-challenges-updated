# # 1) Data Exploration

import urllib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PIL
import seaborn as sns
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder

from sklearn import set_config; set_config(display='diagram')


# ## 1.1) Load data

# - As a datascientist, you don't have access to the full dataset, only the 100k on which you've been tasked to train & finetune the best model)
# - As ML Engineer, you'll have access to the full dataset later, but not for this notebook

DATA_URL = "../data/raw/train_100k.csv"
df = pd.read_csv(DATA_URL)

df.head()

df.info()

# ### 1.1.1) compress data

def compress(df, **kwargs):
    """
    Reduces size of dataframe by downcasting numerical columns
    """
    input_size = df.memory_usage(index=True).sum()/ 1024**2
    print("new dataframe size: ", round(input_size,2), 'MB')

    in_size = df.memory_usage(index=True).sum()
    for type in ["float", "integer"]:
        l_cols = list(df.select_dtypes(include=type))
        for col in l_cols:
            df[col] = pd.to_numeric(df[col], downcast=type)
            if type == "float":
                df[col] = pd.to_numeric(df[col], downcast="integer")
    out_size = df.memory_usage(index=True).sum()
    ratio = (1 - round(out_size / in_size, 2)) * 100

    print("optimized size by {} %".format(round(ratio,2)))
    print("new dataframe size: ", round(out_size / 1024**2,2), " MB")
    return df

df = compress(df, verbose=True)
df.head(1)

# Let's check dtypes optimized

df.dtypes

# We can force optimal dtype directly at loading to minimize RAM!

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

df = pd.read_csv(DATA_URL, dtype=DATA_RAW_DTYPES_OPTIMIZED)
df.info()

# ## 1.2) Clean data

df.describe()

df.shape

# remove redundant columns or rows
df = df.drop(columns=['key'])
df = df.drop_duplicates()
df.shape

df = df.dropna(how='any', axis=0)
df.shape

# remove buggy transactions
df = df[(df.dropoff_latitude != 0) | (df.dropoff_longitude != 0) |
        (df.pickup_latitude != 0) | (df.pickup_longitude != 0)]
df = df[df.passenger_count > 0]
df = df[df.fare_amount > 0]

# Let's check NYC bouding boxes

# load image of NYC map
bouding_boxes = (-74.3, -73.7, 40.5, 40.9)
url = 'https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/nyc_-74.3_-73.7_40.5_40.9.png'
nyc_map = np.array(PIL.Image.open(urllib.request.urlopen(url)))
plt.imshow(nyc_map);

# remove irrelevant/non-representative transactions (rows) for a training set
df = df[df["pickup_latitude"].between(left=40.5, right=40.9)]
df = df[df["dropoff_latitude"].between(left=40.5, right=40.9)]
df = df[df["pickup_longitude"].between(left=-74.3, right=-73.7)]
df = df[df["dropoff_longitude"].between(left=-74.3, right=-73.7)]

df.describe()

# Let's cap training set to reasonable values
df = df[df.fare_amount < 400]
df = df[df.passenger_count < 8]

# ## 1.3) Visualize data

# plot histogram of fare
df.fare_amount.hist(bins=100, figsize=(14,3))
plt.xlabel('fare $USD')
plt.title('Histogram')

# this function will be used more often to plot data on the NYC map
def plot_on_map(df, BB, nyc_map, s=10, alpha=0.2):
    fig, axs = plt.subplots(1, 2, figsize=(16,10))
    axs[0].scatter(df.pickup_longitude, df.pickup_latitude, zorder=1, alpha=alpha, c='red', s=s)
    axs[0].set_xlim((BB[0], BB[1]))
    axs[0].set_ylim((BB[2], BB[3]))
    axs[0].set_title('Pickup locations')
    axs[0].imshow(nyc_map, zorder=0, extent=BB)

    axs[1].scatter(df.dropoff_longitude, df.dropoff_latitude, zorder=1, alpha=alpha, c='blue', s=s)
    axs[1].set_xlim((BB[0], BB[1]))
    axs[1].set_ylim((BB[2], BB[3]))
    axs[1].set_title('Dropoff locations')
    axs[1].imshow(nyc_map, zorder=0, extent=BB)

# plot training data on map
plot_on_map(df, bouding_boxes, nyc_map, s=1, alpha=0.3)

plot_on_map(df, bouding_boxes, nyc_map, s=20, alpha=1.0)

def plot_hires(df, BB, figsize=(12, 12), ax=None, c=('r', 'b')):
    if ax == None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)

    def select_within_boundingbox(df, BB):
        return (df.pickup_longitude >= BB[0]) & (df.pickup_longitude <= BB[1]) & \
            (df.pickup_latitude >= BB[2]) & (df.pickup_latitude <= BB[3]) & \
            (df.dropoff_longitude >= BB[0]) & (df.dropoff_longitude <= BB[1]) & \
            (df.dropoff_latitude >= BB[2]) & (df.dropoff_latitude <= BB[3])

    idx = select_within_boundingbox(df, BB)
    ax.scatter(df[idx].pickup_longitude, df[idx].pickup_latitude, c="red", s=0.01, alpha=0.5)
    ax.scatter(df[idx].dropoff_longitude, df[idx].dropoff_latitude, c="blue", s=0.01, alpha=0.5)

plot_hires(df, (-74.1, -73.7, 40.6, 40.9))

plot_hires(df, (-74, -73.95, 40.7, 40.8))

# ### 1.4) Baseline Score  - preliminary intuitions

def manhattan_distance_vectorized(df: pd.DataFrame, start_lat: str, start_lon: str, end_lat: str, end_lon: str) -> dict:
    """
    Calculate the haverzine and manhattan distance between two points on the earth (specified in decimal degrees).
    Vectorized version for pandas df
    Computes distance in kms
    """
    earth_radius = 6371

    lat_1_rad, lon_1_rad = np.radians(df[start_lat]), np.radians(df[start_lon])
    lat_2_rad, lon_2_rad = np.radians(df[end_lat]), np.radians(df[end_lon])

    dlon_rad = lon_2_rad - lon_1_rad
    dlat_rad = lat_2_rad - lat_1_rad

    manhattan_rad = np.abs(dlon_rad) + np.abs(dlat_rad)
    manhattan_km = manhattan_rad * earth_radius

    return manhattan_km

df['distance'] = manhattan_distance_vectorized(df, "pickup_latitude", "pickup_longitude","dropoff_latitude", "dropoff_longitude")
df['distance'].hist(bins=50)
plt.title("distance (km)")

sns.regplot(data=df, x='distance', y='fare_amount')

from scipy.stats import pearsonr
r2, pvalue = pearsonr(df['distance'], df['fare_amount'])
print(f'{r2=}')
print(f'{pvalue=}')

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
mae = -1*cross_val_score(LinearRegression(), X=df[['distance']], y=df['fare_amount'], scoring='neg_mean_absolute_error').mean()
print(f'{mae=}')

# ☝️ We've got our baseline

df = df.drop(columns=['distance'])
df.shape

# # 2) Preprocessing

# We are given a dataset with only 5 features (passengers + lon/lat), and potentially dozens of millions of rows.
#
# 👉 It make perfect sense to create a lot of "engineered" features such as "hour of the day, etc..."
# - Hundreds of them would cause no problem because the huge number of rows will allow our model to learn all weights associated with these multiple features
# - A dense, deep learning network will be well suited for such case
#
# 👇 The proposed preprocessor:
# - outputs a **fixed** number of features (64) that is independent of the training set.
# - is  **state-less** (i.e it has no `.fit()` method, only a `.transform()`). It can be seen as a *pure function* $f:X \rightarrow X_{processed}$
#
# It will make work much easier for the ML Engineering team.
#

X = df.drop("fare_amount", axis=1)
y = df[["fare_amount"]]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# ## 2.1) Passenger preprocessors

# Let's analyse passengers numbers

sns.histplot(df.passenger_count)

# PASSENGER PIPE
p_min = 1
p_max = 8
passenger_pipe = FunctionTransformer(lambda p: (p-p_min)/(p_max-p_min))

preprocessor = ColumnTransformer(
    [
        ("passenger_scaler", passenger_pipe, ["passenger_count"]),
    ],
)
preprocessor

preprocessor.fit_transform(X_train)

# ## 2.2) Time Preprocessor

# First, let's extract category attributes from the "pickup_datetime"

import math

def transform_time_features(X: pd.DataFrame)->np.ndarray:
    assert isinstance(X, pd.DataFrame)
    pickup_dt = pd.to_datetime(X["pickup_datetime"],
                                format="%Y-%m-%d %H:%M:%S UTC",
                                utc=True)
    pickup_dt = pickup_dt.dt.tz_convert("America/New_York").dt
    dow = pickup_dt.weekday
    hour = pickup_dt.hour
    month = pickup_dt.month
    year = pickup_dt.year
    hour_sin = np.sin(2 * math.pi / 24 * hour)
    hour_cos = np.cos(2*math.pi / 24 * hour)

    return np.stack([hour_sin, hour_cos, dow, month, year], axis=1)

X_time_processed = transform_time_features(X[["pickup_datetime"]])

pd.DataFrame(X_time_processed, columns=["hour_sin", "hour_cos", "dow", "month", "year"]).head()

# Then, one-hot-encode ["day of week", "month"] by forcing all 24*7 combinations of categories to be always present in X_processed (we want a fixed size for X_processed at the end)

time_categories = {
        0: np.arange(0, 7, 1),  # days of the week
        1: np.arange(1, 13, 1)  # months of the year
    }

OneHotEncoder(categories=time_categories, sparse=False)\
    .fit_transform(X_time_processed[:,[2,3]])

# And combine this with rescaling of year

print(df.pickup_datetime.min())
print(df.pickup_datetime.max())

year_min = 2009
year_max = 2019 # Our model may extend in the future

time_pipe = make_pipeline(
    FunctionTransformer(transform_time_features),
    make_column_transformer(
        (OneHotEncoder(
            categories=time_categories,
            sparse=False,
            handle_unknown="ignore"), [2,3]), # correspond to columns ["day of week", "month"], not the others columns
        (FunctionTransformer(lambda year: (year-year_min)/(year_max-year_min)), [4]), # min-max scale the columns 4 ["year"]
        remainder="passthrough" # keep hour_sin and hour_cos
        )
    )

preprocessor = ColumnTransformer(
    [
        ("passenger_scaler", passenger_pipe, ["passenger_count"]),
        ("time_preproc", time_pipe, ["pickup_datetime"]),
    ],
)
preprocessor

pd.DataFrame(preprocessor.fit_transform(X_train)).plot(kind='box');

# ☝️ 23 features approximately centered and scaled

# ## 2.3) Distance pipeline

# Let's add both haversine and manhattan distances as features

lonlat_features = ["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"]

def distances_vectorized(df: pd.DataFrame, start_lat: str, start_lon: str, end_lat: str, end_lon: str) -> dict:
    """
    Calculate the haverzine and manhattan distance between two points on the earth (specified in decimal degrees).
    Vectorized version for pandas df
    Computes distance in kms
    """
    earth_radius = 6371

    lat_1_rad, lon_1_rad = np.radians(df[start_lat]), np.radians(df[start_lon])
    lat_2_rad, lon_2_rad = np.radians(df[end_lat]), np.radians(df[end_lon])

    dlon_rad = lon_2_rad - lon_1_rad
    dlat_rad = lat_2_rad - lat_1_rad

    manhattan_rad = np.abs(dlon_rad) + np.abs(dlat_rad)
    manhattan_km = manhattan_rad * earth_radius

    a = (np.sin(dlat_rad / 2.0)**2 + np.cos(lat_1_rad) * np.cos(lat_2_rad) * np.sin(dlon_rad / 2.0)**2)
    haversine_rad = 2 * np.arcsin(np.sqrt(a))
    haversine_km = haversine_rad * earth_radius

    return dict(
        haversize=haversine_km,
        manhattan=manhattan_km)

def transform_lonlat_features(X:pd.DataFrame)-> np.ndarray:
    assert isinstance(X, pd.DataFrame)
    res = distances_vectorized(X, *lonlat_features)

    return pd.DataFrame(res)

distances = transform_lonlat_features(X[lonlat_features])
distances

dist_min = 0
dist_max = 100

distance_pipe = make_pipeline(
    FunctionTransformer(transform_lonlat_features),
    FunctionTransformer(lambda dist: (dist - dist_min)/(dist_max - dist_min))
    )
distance_pipe

preprocessor = ColumnTransformer(
    [
        ("passenger_scaler", passenger_pipe, ["passenger_count"]),
        ("time_preproc", time_pipe, ["pickup_datetime"]),
        ("dist_preproc", distance_pipe, lonlat_features),
    ],
)
preprocessor

X_processed = pd.DataFrame(preprocessor.fit_transform(X_train))
X_processed.plot(kind='box');

# ☝️ 25 features, approximately scaled

# ## 2.4) GeoHasher

# Finally, let's add information about districts, because some might be more expensive than others
#
# In order to _bucketize_ geospacial information, we'll use `pygeohash`

# !pip install pygeohash

import pygeohash as gh

geohashes = pd.concat([
    X_train.apply(lambda x: gh.encode(x.pickup_latitude, x.pickup_longitude, precision=5), axis=1),
    X_train.apply(lambda x: gh.encode(x.dropoff_latitude, x.dropoff_longitude, precision=5), axis=1),
])

print(len(geohashes.value_counts()))
plt.figure(figsize=(15,5))
plt.plot(np.cumsum(geohashes.value_counts()[:20])/(2*len(X_train))*100)
plt.title("percentage of taxi rides from/to these districts");

# ☝️ Only the 20 first district matters. We can one hot encode these ones

most_important_geohash_districts = np.array(geohashes.value_counts()[:20].index)
most_important_geohash_districts

def compute_geohash(X:pd.DataFrame, precision:int = 5) -> np.ndarray:
    """
    Add a geohash (ex: "dr5rx") of len "precision" = 5 by default
    corresponding to each (lon,lat) tuple, for pick-up, and drop-off
    """
    assert isinstance(X, pd.DataFrame)

    X["geohash_pickup"] = X.apply(lambda x: gh.encode(
        x.pickup_latitude, x.pickup_longitude, precision=precision),
                                    axis=1)
    X["geohash_dropoff"] = X.apply(lambda x: gh.encode(
        x.dropoff_latitude, x.dropoff_longitude, precision=precision),
                                    axis=1)
    return X[["geohash_pickup", "geohash_dropoff"]]

geohash_categories = {
    0: most_important_geohash_districts,  # pickup district list
    1: most_important_geohash_districts  # dropoff district list
}

geohash_pipe = make_pipeline(
    FunctionTransformer(compute_geohash),
    OneHotEncoder(categories=geohash_categories,
                  handle_unknown="ignore",
                  sparse=False))
geohash_pipe

# ## 2.5) Full Preprocessing pipeline

# COMBINED PREPROCESSOR
final_preprocessor = ColumnTransformer(
    [
        ("passenger_scaler", passenger_pipe, ["passenger_count"]),
        ("time_preproc", time_pipe, ["pickup_datetime"]),
        ("dist_preproc", distance_pipe, lonlat_features),
        ("geohash", geohash_pipe, lonlat_features),
    ],
    n_jobs=-1,
)
final_preprocessor

X_train_processed = final_preprocessor.fit_transform(X_train)

fig, ax = plt.subplots(figsize=(10,5))
pd.DataFrame(X_train_processed).plot(kind='box', ax=ax);

fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(pd.DataFrame(X_train_processed).corr(), vmin=-1, cmap='RdBu');

# To conclude, we compress our data to float32

X_train_processed.dtype

print(X_train_processed.nbytes / 1024**2, "MB")

# compress a bit the data
X_train_processed = X_train_processed.astype(np.float32)
print(X_train_processed.nbytes / 1024**2, "MB")

# # 3) Model

# ## 3.1) Architecture

from tensorflow import keras
from tensorflow.keras import Model, Sequential, layers, regularizers
from tensorflow.keras.callbacks import EarlyStopping

def initialize_model(X: np.ndarray) -> Model:
    """
    Initialize the Neural Network with random weights
    """

    reg = regularizers.l1_l2(l2=0.01)

    model = Sequential()
    model.add(layers.BatchNormalization(input_shape=X.shape[1:]))
    model.add(layers.Dense(100, activation="relu", kernel_regularizer=reg, input_shape=X.shape[1:]))
    model.add(layers.BatchNormalization())

    model.add(layers.Dense(50, activation="relu", kernel_regularizer=reg))
    model.add(layers.BatchNormalization())

    model.add(layers.Dense(10, activation="relu"))
    model.add(layers.BatchNormalization(momentum=0.99)) # use momentum=0 for to only use statistic of the last seen minibatch in inference mode ("short memory"). Use 1 to average statistics of all seen batch during training histories.

    model.add(layers.Dense(1, activation="linear"))

    print("✅ model initialized")

    return model

model = initialize_model(X_train_processed)
model.summary()

learning_rate = 0.001
batch_size = 256

optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
model.compile(loss="mean_squared_error", optimizer=optimizer, metrics=["mae"])

es = EarlyStopping(monitor="val_loss",
                    patience=2,
                    restore_best_weights=True,
                    verbose=0)

history = model.fit(X_train_processed,
                    y_train,
                    validation_split=0.3,
                    epochs=100,
                    batch_size=batch_size,
                    callbacks=[es],
                    verbose=1)

# ## 3.2) Performance evaluation

X_test_processed = final_preprocessor.transform(X_test)

y_pred = model.predict(X_test_processed)

model.evaluate(X_test_processed, y_test)

plt.figure(figsize=(15,8))
import seaborn as sns
import matplotlib.pyplot as plt
plt.hist(y_pred, label='pred', color='r', bins=200, alpha=0.3)
plt.hist(y_test, label='truth', color='b', bins=200, alpha=0.3)
plt.legend()
plt.xlim((0,60))

residuals.describe()

residuals = y_pred - y_test
sns.histplot(residuals)
plt.xlim(xmin=-20, xmax=20)

residuals.sort_values(by='fare_amount')

# Residual vs. Actual scatter plot
plt.figure(figsize=(15,5))
plt.scatter(x=y_test,y=residuals, alpha=0.1)
plt.xlabel('actual')
plt.ylabel('residuals')

# Residual vs. Actual scatter plot
plt.figure(figsize=(15,5))
plt.scatter(x=y_pred,y=residuals, alpha=0.1)
plt.xlabel('predicted')
plt.ylabel('residuals')

# ☝️ Our model has MAE of about 2$ per course, compared with a mean course price of 11$.
#
# A simple linear regression would give us about 2.5$ of MAE, but the devil lies in the details!
#
# In particular, we're not that good at predicting very long / expensive courses

# # 🧪 Test your understanding

# ❓ Try answer these questions with your buddy
# - [ ] Are you satisfied with the model performance ?
# - [ ] What is a state-less pipeline (as opposed to state-full) ?
# - [ ] How does a OHEncoder works with fixed column categories ?
# - [ ] How is the data-normalization done in the Neural Net ?

# ❓ Predict the price for this new course `X_new` below and store the result `y_new` **as a `float`**

X_new = pd.DataFrame(dict(
    key=["2013-07-06 17:18:00"],  # useless but the pipeline requires it
    pickup_datetime=["2013-07-06 17:18:00 UTC"],
    pickup_longitude=[-73.950655],
    pickup_latitude=[40.783282],
    dropoff_longitude=[-73.984365],
    dropoff_latitude=[40.769802],
    passenger_count=[1]))
X_new

pass  # YOUR CODE HERE

from nbresult import ChallengeResult
import os

result = ChallengeResult('notebook',subdir='train_at_scale',
    y_new=y_new
)
result.write()
print(result.check())

#


