
[//]: # ( challenge tech stack: cloud-storage gsutil big-query bq )

[//]: # ( challenge presentation )

Now that your machine is setup for GCP, let's upload the _TaxiFare_ dataset to the cloud.

In this challenge, we will discover the first two pillar products of the **Google Cloud Platform** suite:
- We will explore **Cloud Storage**, which acts as a disk in the cloud, to store the training and validation datasets in the cloud as static content
- We will then switch to **Big Query**, our first data warehouse, which will allow us to consume and update the datasets iteratively much easier

👉 Big Query will allow the package training the model iteratively to process the data by chunks much easier

**💻 Remember to install the package of the current challenge with `make reinstall_package`**

💡 Out of curiosity, you can always verify the version of the package installed with `pip show taxifare-model`

**💻 Do not forget to handle your `.env` file (_copy_ the `.env.sample`, _fill_ the `.env`, _allow_ `direnv`)...**

[//]: # ( challenge instructions )

## Upload the dataset to the cloud

In the previous unit, you trained the _TaxiFare_ model on your machine.

From now on, we will be running the training in the cloud. We need our dataset to be stored in the cloud as well.

There are a few options here. Let's explore storing our raw dataset as a **CSV** file using **Cloud Storage**.

**❓ How do you store your CSV dataset in the cloud ?**

⚠️ The goal here is not to challenge your internet connection, so we will not have you wait while all your classmates simultaneously try to upload the 170GB of the _TaxiFare_ dataset to their own GCP bucket 🙌

We only want to see how you would do that, so we will be working with a sample 10k dataset.

Download the [sample 10k training dataset](https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_10k.csv) and the [sample 10k validation dataset](https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/val_10k.csv) on your machine.

Then find the `gsutil` command allowing you to upload these datasets to your **bucket**.

**💻 Upload the `train_10k.csv` and `val_10k.csv` files to your bucket as `data/train_10k.sample.csv` and `data/val_10k.sample.csv` blobs**

**🧪 Run the tests with `make dev_test`**

👉 `test_cloud_data_uploaded_blob` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  There is a command for everything. You may use `curl` to download the data:

  ``` bash
  curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_10k.csv > train_10k.csv
  curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/val_10k.csv > val_10k.csv
  ```
</details>

Cloud Storage is great to store static data such as images and videos, but we want to train our model iteratively. In order to do that, we need to consume the data by chunks, which Cloud Storage allows to do using `pandas.read_csv`. But we also need to store data iteratively since the preprocessed training data is processed by chunks. And Cloud Storage does not make this easy on us since the blobs stored are immutable. So we would need to upload the full preprocessed training CSV each time we process a new chunk. Let's use Big Query instead !

👉 The training and validation datasets are structured. Moreover we need to consume and update our data iteratively. Using a database in the cloud is ideal for this task. Our package will be able to store the preprocessed chunks of the training set progressively as they are processed.

## Build your first data warehouse

**❓ How do you create a dataset in a data warehouse ?**

Let's upload our sample 10k datasets CSV to **Big Query**.

**💻 Find the `bq` command allowing you to create a new _dataset_. Create a dataset and add 2 new _tables_ `train_10k` and `val_10k` into the dataset, one for our training set and another for our validation set.**

Note how in Big Query a *dataset* can contain several sets of data stored as *tables*.

**📝 Fill the `DATASET` variable in the `.env` project configuration**

**🧪 Run the tests with `make dev_test`**

👉 `test_cloud_data_create_dataset` and `test_cloud_data_create_table` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  Although the `bq` command is a child of the **Google Cloud SDK** that you installed on your machine, it does not seem to be follow the same help pattern as the `gcloud` and `gsutil` commands.

  Try running `bq` without arguments to list the available sub commands.

  What you are looking for is probably in the `mk` (make) section.
</details>

Now that you have a Big Query dataset with tables, let's populate them with our sample 10k CSVs.

**❓ How do you upload data to a dataset in a data warehouse ?**

Find the `bq` command allowing you to upload a CSV to a dataset table.

**💻 Upload the `train_10k.csv` and `val_10k.csv` files to your dataset tables**

Make sure that the _datasets_ that you create use the following data types:
- `key` and `pickup_datetime`: _timestamp_
- `fare_amount`, `pickup_longitude`, `pickup_latitude`, `dropoff_longituden` and `dropoff_latitude`: _float_
- `passenger_count`: _integer_

**🧪 Run the tests with `make dev_test`**

👉 `test_cloud_data_table_content` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  The command will probably ask you to provide a schema for the data that you are uploading to your table (remember that we have not provided a schema for the table yet).

  In order to do that, the first option would be to have a look at the header of the CSV.

  The `head -n 11 train_10k.csv` command showing the first 11 lines of any file can be useful in order to glance at the top of the CSV (its buddy is the `tail` command).

  Once you have retrieved the list of columns, you need to define the data type that you want to use for of each of the columns (search for *big query schema data types*).

  Then you would provide the full schema of the table as an argument to the command with `--schema "key:timestamp,fare_amount:float,..."`

  This is a little cumbersome, but there are situations where you will want to specify the schema manually.

  ... Of course there is always the option to search for a parameter of the command that would do all that work for you 😉
</details>

## Train locally from data in Big Query

Now that our data is in the cloud, we will adapt the code of our package in order to source the data chunks used for the training from Big Query.

The code of the model iterative training is detailed below. Take the time to read the following paragraphs until you are confident with the way the package works. Do not hesitate to call a TA if anything in the code is unclear.

**❓ How do you train your model incrementally from Big Query ?**

Let's have a look at the new structure of the code:
- The `taxifare_model.interface.main` module is the entry point of the package. In order to run an iterative training, it provides the `preprocess` and `train` _functions_.
- The `preprocess` function is responsible for preprocessing the full dataset from the data source chunk by chunk. For each chunk of data in the data source, it retrieves it, preprocesses it, and stores it back in the data source in a different location.
- The `train` function on its end retrieves all the _preprocessed data_ from the data source chunk by chunk, and trains the model with each chunk.

### Step 1: `preprocess` retrieves the data

The `preprocess` and `train` _functions_ have no idea what the data source is (local or in the cloud) or how to interact with it. They delegate this role to the `get_chunk` and `save_chunk` _functions_ imported from `data.py`.

In `main.py`, we see that the `preprocess` _function_ will iterate using `while (True)` until the `get_chunk` _function_ returns `None`. Since `preprocess` does not know the size of the dataset in advance, it is up to `get_chunk` to tell `preprocess` to stop iterating by returning `None`.

``` python
def preprocess(
    first_row=0
):
    """
    Preprocess the dataset by chunks fitting in memory.
    """

    print("\n⭐️ use case: preprocess")

    # iterate on the dataset, by chunks
    chunk_id = 0

    while (True):

        print(Fore.BLUE + f"\nProcessing chunk n°{chunk_id}..." + Style.RESET_ALL)

        data_chunk = get_chunk(source_name=f"train_{DATASET_SIZE}",
                               index=(chunk_id * CHUNK_SIZE) + first_row,
                               chunk_size=CHUNK_SIZE)

        # Break out of while loop if data is none
        if data_chunk is None:
            print(Fore.BLUE + "\nNo data in latest chunk..." + Style.RESET_ALL)
            break

        # ... preprocess and save data ...

        chunk_id += 1

    # ...
```

Each call to the `get_chunk` function takes as parameter:

**The name of the data source to use**

The `DATASET_SIZE` variable in `main.py` is imported from the `taxifare_model.ml_logic.params` module:

``` python
from taxifare_model.ml_logic.params import (CHUNK_SIZE,
                                            DATASET_SIZE,
                                            VALIDATION_DATASET_SIZE)
```

In `params.py`, the variable is loaded from the environment:

``` python
DATASET_SIZE = os.environ.get("DATASET_SIZE")
```

Since we setup `direnv`, the value of the `DATASET_SIZE` environment variable is loaded from the value filled in the `.env` file.

👉 So the idea is that you can change the dataset used by the package by changing the value of the `DATASET_SIZE` variable in the `.env` file, as long as the resource with a corresponding name (csv or dataset table) from which to read the data exists in the data source

**The index of the chunk**

The `preprocess` function starts at `0` and increments the index at each call to `get_chunk` in order to let `get_chunk` know what chunk of data to retrieve.

**The chunk size**

Again, the `CHUNK_SIZE` variable is imported from `params.py` and loaded from the `.env` file by `direnv`.

👉 Changing the `CHUNK_SIZE` in the `.env` file allows you to play with the size of the chunks and experiment on their impact on the training time (you can use any value)

**Return value**

The `get_chunk` _function_ returns the retrieved data chunk, or `None` if there is no more data to retrieve.

👉 Note that the last chunk retrieved may not correspond to the `CHUNK_SIZE` if the number of observations in the data source is not a multiple of `CHUNK_SIZE`

### Step 2: `preprocess` saves the preprocessed data

Once a chunk has been preprocessed, the `preprocess` _function_ saves the preprocessed data back to the data source using the `save_chunk` _function_ imported from `data.py`.

👉 The idea of saving the preprocessed data back to the data source is to avoid reprocessing in the future the raw data in the eventuality that the preprocessing is very time consuming (a _geocoding_ for example). This is particularly true for Deep Learning models which make several passes over the dataset (epochs)

``` python
def preprocess(
    first_row=0
):
    """
    Preprocess the dataset by chunks fitting in memory.
    """

    print("\n⭐️ use case: preprocess")

    # iterate on the dataset, by chunks
    chunk_id = 0

    while (True):

        print(Fore.BLUE + f"\nProcessing chunk n°{chunk_id}..." + Style.RESET_ALL)

        data_chunk = get_chunk(source_name=f"train_{DATASET_SIZE}",
                               index=(chunk_id * CHUNK_SIZE) + first_row,
                               chunk_size=CHUNK_SIZE)

        # Break out of while loop if data is none
        if data_chunk is None:
            print(Fore.BLUE + "\nNo data in latest chunk..." + Style.RESET_ALL)
            break

        # ... preprocess data ...

        # save and append the chunk
        is_first = chunk_id == 0 and first_row == 0

        save_chunk(source_name=f"train_processed_{DATASET_SIZE}",
                   is_first=is_first,
                   data=data_processed_chunk)

        chunk_id += 1

    # ...
```

The `save_chunk` _function_ takes as parameters:

**The name of the data source**

Note that the name of the data source location to which the preprocessed data is saved obviously differs from the one in which the data is read.

**Whether the processed chunk saved is the first chunk**

Can you think of a data source type for which it would make sense to know whether the chunk saved is the first one ?

👉 That's right, when writing a CSV, it matters in order to know whether the header should be written as the first line of the file or not. You do not want to ommit the header for the first chunk of data saved. And you do not want to add the header in the middle of the CSV file when you save additional chunks of data.

**The data to save**

Of course we need to pass to the function the chunk of data to save.

### Step 3: `train` retrieves the preprocessed data

The `train` _function_ starts by using `get_chunk` in order to retrieve the full validation dataset (note the `chunk_size=None` parameter).

👉 This is an additional spec: the `get_chunk` function should return the whole dataset if `chunk_size` is `None` (you can expect the user of the function to know what they are doing)

``` python
def train(
    first_row=0):
    """
    Train a new model on the full (already preprocessed) dataset ITERATIVELY, by loading it
    chunk-by-chunk, and updating the weight of the model after each chunks.
    Save final model once it has seen all data, and compute validation metrics on a holdout validation set
    common to all chunks.
    """

    print("\n⭐️ use case: train")

    print(Fore.BLUE + "\nLoading preprocessed validation data..." + Style.RESET_ALL)

    # load a validation set common to all chunks, used to early stop model training
    data_val = get_chunk(source_name=f"val_{VALIDATION_DATASET_SIZE}",
                         index=0,  # retrieve from first row
                         chunk_size=None)  # retrieve all further data

    if data_val is None:
        print("\n✅ no data to train")
        return None

    # ...
```

Appart from that, the `train` _function_ works similarly to the `preprocess` _function_: it iterates on the chunks of the **preprocessed** data source until there is no more data to process.

``` python
def train(
    first_row=0):
    """
    Train a new model on the full (already preprocessed) dataset ITERATIVELY, by loading it
    chunk-by-chunk, and updating the weight of the model after each chunks.
    Save final model once it has seen all data, and compute validation metrics on a holdout validation set
    common to all chunks.
    """

    # ... load validation set and other initialization ...

    # iterate on the full dataset per chunks
    chunk_id = 0

    while (True):

        print(Fore.BLUE + f"\nLoading and training on preprocessed chunk n°{chunk_id}..." + Style.RESET_ALL)

        data_processed_chunk = get_chunk(source_name=f"train_processed_{DATASET_SIZE}",
                                         index=(chunk_id * CHUNK_SIZE) + first_row,
                                         chunk_size=CHUNK_SIZE)

        # check whether data source contain more data
        if data_processed_chunk is None:
            print(Fore.BLUE + "\nNo more chunk data..." + Style.RESET_ALL)
            break

        # ... train the model ...

        chunk_id += 1

    # ...
```

👉 You have now seen how the `preprocess` and `train` functions are able to work with data from a data source that they know nothing about (if it is local or in the cloud), nor do they have any idea how to deal with (using **Big Query** code vs `pandas`)

This is the strength of the _separation of concerns_: the code in `main.py` needs only care about the global logic it is implementing (iterating through data chunks, preprocessing each chunk, training the model on the chunk), and not about the details of implementation of each task.

We will see right away how these details are implemented: let's jump to the `get_chunk` and `save_chunk` _functions_ in `data.py`.

### Step 4: `data.py` acts as a switch

The beauty of having all the global logic implemented in `main.py` is that in `data.py` we need not worry about the context in which the functions are called. We only need to concentrate on what each function does and how it does it.

Let's have a look at the `get_chunk` _function_ in order to convince ourselves of this (the `save_chunk` _function_ works similarly).

The role of the `get_chunk` _function_ is to decide whether to source data from the local disk or from the data warehouse depending on the value of the `DATA_SOURCE` variable in the `.env` file. And then to call the appropriate package _module_ to interact with the data source and retrieve a data chunk.

``` python
def get_chunk(source_name: str,
              index: int = 0,
              chunk_size: int = None) -> pd.DataFrame:
    """
    return a chunk of the dataset between `index` and `index + chunk_size - 1`
    """

    if "processed" in source_name:
        columns = None
        dtypes = DATA_PROCESSED_DTYPES_OPTIMIZED
    else:
        columns = DATA_RAW_COLUMNS
        dtypes = DATA_RAW_DTYPES_OPTIMIZED

    if os.environ.get("DATA_SOURCE") == "big query":

        chunk_df = get_bq_chunk(table=source_name,
                                index=index,
                                chunk_size=chunk_size,
                                dtypes=dtypes)

        return chunk_df

    chunk_df = get_pandas_chunk(path=source_name,
                                index=index,
                                chunk_size=chunk_size,
                                dtypes=dtypes,
                                columns=columns)

    return chunk_df
```

The `get_chunk` _function_ uses the `DATA_SOURCE` environment variable loaded from the `.env` file in order to know whether to use the local disk `DATA_SOURCE == local` or _Big Query_ `DATA_SOURCE == big query` as a data source.

It then calls the appropriate function to do the job: either `get_pandas_chunk` to load data from the local disk or `get_bq_chunk` to load data from Big Query.

Note that `get_bq_chunk` takes as parameter a `dtypes` which is a dictionary of expected data types for the returned data chunk, while `get_pandas_chunk` additionally requires a list of `columns` used in order to build the returned `DataFrame`.

The `get_pandas_chunk` _function_ is located in the `local_disk` _module_. You will need to add imports for the `get_bq_chunk` _function_ yourself:

``` python
from taxifare_model.data_sources.local_disk import (get_pandas_chunk,
                                                    save_local_chunk)
```

In the design that we choose the `data_py` only acts as a switch. It is not aware of the context in which the `get_chunk` and `save_chunk` functions are called by `preprocess` or `train` in `main.py`. Its does not know the details of implementation of retrieving or saving data from or to a data source.

The goal here was to split the logic in several pieces in order to simplify the problem that we solve:
- `taxifare_model.interface.main` handles the global logic
- `taxifare_model.ml_logic.data` determines which data source should be used
- `taxifare_model.data_sources.big_query` is responsible for exchanging data with _Big Query_
- `taxifare_model.data_sources.local_disk` is responsible for exchanging data with the local disk using `pandas`

We provide you with the code of the `taxifare_model.data_sources.local_disk` _module_ so you can see how the `get_pandas_chunk` and `save_local_chunk` are working.

👉 Go have a look at the code in `local_disk.py`

### Step 5: `big_query.py` is where to code

At last here is the place where you should work: the `taxifare_model.data_sources.big_query` _module_ contains the `get_bq_chunk` and `save_bq_chunk` methods that you need to implement.

These methods are called by `get_chunk` and `save_chunk` in `data.py` when the `.env` file contains the variable `DATA_SOURCE` set to `big query`.

The role of `get_bq_chunk` is to retrieve a chunk of data from a Big Query table given its first row _index_ and the number of rows (_chunk_size_) to retrieve. The function also takes a `dtypes` argument containing a dictionnary of expected data types in the returned `DataFrame`.

**💻 Set the `DATA_SOURCE` variable in the `.env` file to source data from Big Query. Complete the `get_bq_chunk` and `save_bq_chunk` functions in the `taxifare_model.data_sources.big_query` module. Add the required imports in `data.py`**

**🧪 Run the tests with `make dev_test`**

👉 `test_cloud_data_bq_chunks` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  If you look for *Paging through data table* in Big Query, or have a look at the [Big Query python API reference](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.client.Client.html), you should identify a method allowing you to retrieve the rows of a query one chunk after the next.
</details>

You can now train you model from the cloud using data chunks retrieved from Big Query 🎉

⚙️ **Train your model with data from Big Query and time the outcome ⏰**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You can time the duration of a command by prefixing it with the `time` command:

  ``` bash
  time python -m taxifare_model.interface.main
  ```

  The timing appears after the command output (more help on the _time_ command with `man time`).
</details>

👉 Observe how the duration of the training varies when you source the data from Big Query versus when the data is stored on your machine.

🏁 Congrats! You have adapted your package to be able to source data incrementally in the cloud from either Cloud Storage or Big Query.
