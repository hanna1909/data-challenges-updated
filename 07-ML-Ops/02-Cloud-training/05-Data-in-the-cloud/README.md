
[//]: # ( challenge tech stack: cloud-storage gsutil big-query bq )

[//]: # ( challenge presentation )

Now that your machine is ready, let's use GCP in order to upload the dataset to the cloud.

In this challenge, we will discover the first two pillar products of the **Google Cloud Platform** suite:
- **Cloud Storage**, which acts as a disk in the cloud, will allow us to store the training and validation datasets in the cloud
- **Big Query**, our first data warehouse, will allow us to store the training and validation datasets as an alternative data source

**💻 Remember to install the package of the current challenge with `make reinstall_package`**

💡 Do not forget that you can always verify the version of the package installed with `pip show taxifare-model`

[//]: # ( challenge instructions )

## Upload the dataset to the cloud

In the previous unit, you trained the `TaxiFare` model on your machine.

From now on, we will be running the training in the cloud. We need our dataset to be stored in the cloud as well.

There are a few options here. Let's explore storing our raw dataset as a **CSV** file using **Cloud Storage**.

**❓ How do you store your CSV dataset in the cloud ?**

⚠️ The goal here is not to challenge your internet connection, so we will not have you wait while all your classmates simultaneously try to upload the 170GB of the `TaxiFare` dataset to their GCP bucket 🙌

We only want to see how you would do that, so we will be working with a sample 10k dataset.

Download the [sample 10k training dataset](https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_10k.csv) and the [sample 10k validation dataset](https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/val_10k.csv) on your machine.

Find the `gsutil` command allowing you to upload the `TaxiFare` dataset to your **bucket**.

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

## Train locally from data in Cloud Storage

In the previous unit, you trained your `taxifare_model` package incrementally using a CSV stored on your machine.

Now we want to be able to perform this incremental training using the data we stored in Cloud Storage.

**❓ How do you train your model incrementally from Cloud Storage ?**

Training incrementally means that we need to retrieve the data from our data source chunk by chunk so that there is enough memory on our machine to handle the whole dataset in several passes.

We added the `get_pandas_chunk` function to the package. The role of `get_pandas_chunk` is to retrieve a chunk of data from a Cloud Storage CSV file given its first row _index_ and the number of rows (_chunk_size_) to retrieve.

You can now train you model from the cloud using data chunks retrieved from Cloud Storage 🎉

**⚙️ Train your model with data from Cloud Storage and time the outcome ⏰**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You can time the duration of a command by prefixing it with the `time` command:

  ``` bash
  time python -m taxifare_model.interface.main
  ```

  The timing appears after the command output (more help on the _time_ command with `man time`).
</details>

👉 observe how the training with data from Cloud Storage takes more time than training using data on your machine. This is because your code is fetching data over the network for each chunk

## Build your first data warehouse

Training our model from the CSV stored in Cloud Storage is a perfectly valid option.

Another option you may encounter when training data is to use a data warehouse. In particular when you are working with a **Data Engineer** who will build and maintain a data pipeline in order to give you access to the data.

While Cloud Storage allows to deal with large volumes of binary data (images, sound or videos), Biq Query thrives to handle large volumes of text data.

**❓ How do you create a dataset in a data warehouse ?**

We will not explore data pipelines here, let's just upload our sample 10k dataset CSV to **Big Query** to get a taste of the drill.

**💻 Find the `bq` command allowing you to create a new _dataset_. Create a dataset and add 2 new _tables_ `train_10k` and `val_10k` into the dataset, one for our training set and another for our validation set.**

Note how in Big Query a *dataset* can contain several sets of data stored as *tables*.

**📝 Fill the `DATASET` variable the `.env` project configuration**

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

  ... Of course there is always the solution to identify a parameter of the command that would do all that work for you 😉
</details>

## Train locally from data in Big Query

Let's verify that our package trains as well from data in Big Query as from blobs stored on Cloud Storage.

**❓ How do you train your model incrementally from Big Query ?**

We added the `get_bq_chunk` function to the `taxifare_model.data_sources.big_query` module. The role of `get_bq_chunk` is to retrieve a chunk of data from a Big Query table given its first row _index_ and the number of rows (_chunk_size_) to retrieve. The function also takes a `dtypes` argument containing a dictionnary of expected data types in the returned `DataFrame`.

**💻 Complete the `get_bq_chunk` function in the `taxifare_model.data_sources.big_query` module**

**🧪 Run the tests with `make dev_test`**

👉 `test_cloud_data_bq_chunks` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  If you look for *Paging through data table* in Big Query, or have a look at the [Big Query python API reference](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.client.Client.html), you should identify a method allowing you to retrieve the rows of a query one chunk after the next.
</details>

You can now train you model from the cloud using data chunks retrieved from Big Query 🎉

⚙️ **Train your model with data from Big Query and time the outcome ⏰**

👉 training with data from Big Query is even slower than using data from Cloud Storage. You can speed up the training by using a larger _chunk_size_ in order to reduce the overhead of calling Big Query

🏁 Congrats! You have adapted your package to be able to source data incrementally in the cloud from either Cloud Storage or Big Query.
