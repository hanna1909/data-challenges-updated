
[//]: # ( presentation of the unit )

# 🪐 Enter the dimension of Cloud Computing! 🚀

In the previous unit, you have **packaged** 📦 the notebook of the _WagonCab_ data science team. And you updated the code so that the model can be trained on the _TaxiFare_ **full dataset** 🗻.

In this unit, you will learn how to grow from a **Data Scientist** into a **ML Engineer** 🤩

A _Data Scientist_ does all their research work on a single machine, either their local machine or a machine in the cloud through a hosted service such as **Colab** for example.

A _ML Engineer_ knows how to dispatch their work to several machines and use a pool of **cloud resources**, remote storage or processing capacities, as their playground.

You will discover how to split your work into jobs executed on multiple machines in the cloud, so that manually trigerring the execution of your code is no longer a bottleneck for the model lifecycle.

You will learn how to drive a remote machine in a data center located anywhere in the world! Or in space if you find a cloud provider that offers capacity there 👽

The resources of the cloud will be accessible at your fingertips, through a _Graphical User Interface_ for exploration using the **[web console 🌍](https://console.cloud.google.com/)**, through a **[terminal](https://en.wikipedia.org/wiki/Terminal_emulator)** 💻 to gain speed and efficiency, or through **code** 📝 when you want to automate your work.

[//]: # ( unit tech stack: gcloud gsutil cloud-storage compute-engine mlflow vertex-ai )

[//]: # ( presentation of the challenges of the unit )

# 1️⃣ PROJECT STRUCTURE

Discover the file and directory **structure** of the challenges that you will be tackling for the rest of the module.

<details>
  <summary markdown='span'><strong>❓Instructions (expand me)</strong></summary>

[//]: # ( challenge tech stack: )

[//]: # ( challenge presentation )

🚨 Each new challenge will bring in an additional set of features on which to work

👉 From now on, you will start each new challenge with the solution of the previous challenge

❓ Now, read carefully the following document to discover the structure of the challenges

[//]: # ( challenge instructions )

## Project structure

Here are the main files of interest:

```bash
.                                   # challenge root
├──taxifare
│   ├── data_sources
│   │   ├── big_query.py            # ☁️ cloud data storage client
│   │   └── local_disk.py           # 🚚 data exchange functions
│   ├── interface
│   │   └── main.py            # 🚪 (new) entry point
│   └── ml_logic
│       ├── __init__.py
│       ├── data.py                 # 📦 data storage interface
│       ├── encoders.py
│       ├── model.py
│       ├── params.py
│       ├── preprocessor.py
│       ├── registry.py             # 📦 model storage functions
│       └── utils.py
├── tests                           # 🧪 tests
├── .env.sample                     # ⚙️ sample `.env` file containing the variables used in the challenge
├── .envrc                          # 🎬 .env loader (used by `direnv`)
├── Makefile
├── requirements.txt
└──  setup.py
```

### ⚙️ `.env.sample`

This file is a _template_ allowing you to create the `.env` file for each challenge. The `.env.sample` file contains the variables required by the code and expected in the `.env` file. 🚨 Keep in mind that the `.env` file **should never be stored in Git** and we have added it to your `.gitignore`.

### 🚪 `main.py`

Bye bye `taxifare.interface.main_local` module, you served us well ❤️

Long live `taxifare.interface.main`, our new package entry point ⭐️ to:
- ~~`preprocess_and_train`~~: This method have been deleted: it does not scale well enough as we saw previously.
- `preprocess`: preprocess the data by chunk and store data_processed
- `train`: train the data by chunk and store model weights
- `evaluate`: evaluate the performance of the latest trained model on new data
- `pred`: make a prediction on a `DataFrame` with a specific version of the trained model

🚨 One main change in the code of the package is that we choose to delegate some of its work to dedicated modules in order to limit the size of the `main.py` file.

The code of the model, the preprocessing and the data cleaning files does not change 👌

The main changes concern :
- The project configuration: the code loads the application configuration from the environment variables loaded by direnv from the .env file
- The model storage: the code evolves to store the trained model either locally - or _spoiler alert_ in the cloud
- The training data: the code uses the `data.py` module as an _interface_ to other modules that load the data either from a local data source or from the cloud depending on the `.env` configuration

### Data delegation: 📦 `data.py` + 🚚 `local_disk.py` + ☁️ `big_query.py`

- `ml_logic.data` is now responsible for data cleaning
- `data_sources.local_disk` is responsible for loading from and saving data to your local disk
- `data_sources.big_query` is responsible for loading from and saving data to BigQuery

**💡`data.py` now acts as a switch** The beauty of having all the global logic implemented in `main.py` is that in `data.py` we need not worry about the context in which the functions are called. We only need to concentrate on what each function does and how it does it.

- Pay attention to the `ml_logic.data.get_chunk` _function_ in order to undertand how it can switch from local to cloud data loading (the `save_chunk` _function_ works similarly for storage).

- We provide you with the code of the `data_sources.local_disk` _module_ so you can see how the `get_pandas_chunk` and `save_local_chunk` are working. Later on, we will code the equivalent for big query instead of local data storage.

✋ Ask for a TA if you need explanations to understand any of the above steps.

</details>
<br>

# 2️⃣ ENVIRONMENT

Learn how to setup the **application parameters** for your challenges

<details>
  <summary markdown='span'><strong>❓Instructions (expand me)</strong></summary>


[//]: # ( challenge tech stack: direnv )

[//]: # ( challenge instructions )

## Install `taxifare` version `0.0.4`

**💻 Install the new package version**
```bash
make reinstall_package
```

**🧪 Check the package version**
```bash
pip list | grep taxifare
# taxifare               0.0.4
```

## Configuration setup

Our goal is to be able to configure the behavior of our _package_ 📦 depending on the value of the variables defined in a `.env` project configuration file.

In order to do so, we will install the `direnv` shell extension. Its job is to locate the nearest `.env` file in the parent directory structure of the project and load its content into the environment.

<details>
  <summary markdown='span'><strong> ⚙️ macOS </strong></summary>


  ``` bash
  brew install direnv
  ```
</details>

<details>
  <summary markdown='span'><strong> ⚙️ Ubuntu (Linux or Windows WSL2) </strong></summary>


  ``` bash
  sudo apt update
  sudo apt install -y direnv
  ```
</details>

Once `direnv` is installed, we need to tell `zsh` to load `direnv` whenever it starts. This will allow `direnv` to monitor the changes in the `.env` project configuration, and to refresh the `environment variables` accordingly.

You need to update your `~/.zshrc` file in order to tell it to load `direnv`.

**💻 Add `direnv` to the list of `zsh` plugins**

Open the resources files:

``` bash
code ~/.zshrc
```

The list of plugins is located at the start of the files and should look this this when you add `direnv`:

``` bash
plugins=(git gitfast last-working-dir common-aliases zsh-syntax-highlighting history-substring-search pyenv direnv)
```

**💡 Start a new `zsh` window in order to load `direnv`**

**💻 At this point `direnv` is still not able to load anything: there is no `.env` file, let's do this:**

- Copy the `env.sample` file and rename it as `.env`
- Enable the project configuration with `direnv allow .` (the `.` stands for _current directory_)
- You can retrieve info on how `direnv` works any time by running `direnv --help`

**🧪 Check `direnv` is able to read the environment variable from the `.env` file:**
```bash
echo $LOCAL_DATA_PATH
# path/to/the/local/data
```

## Update your `.env` project configuration

From now on, whenever you need to update the behavior of the project, you will be able to change its parameters by simply editing the `.env` project configuration.

**Keep data size values small for this unit, for dev purposes**
```bash
DATASET_SIZE=10k
VALIDATION_DATASET_SIZE=10k
CHUNK_SIZE=6000
```

**📝 Fill the following**
- `LOCAL_DATA_PATH` variable in the `.env` project configuration with `~/.lewagon/mlops/data`
- `LOCAL_REGISTRY_PATH` variable in the `.env` project configuration with `~/.lewagon/mlops/training_outputs`

**🧪 Check your env variables manually**
```bash
echo $LOCAL_DATA_PATH
echo $LOCAL_REGISTRY_PATH
# ~/.lewagon/mlops/data
# ~/.lewagon/mlops/training_outputs
```

**🧪 Check your env variable automatically**
``` bash
make show_env
```
👉 How does that work ? Very simple: the `show_env` command in the `Makefile` just runs an `echo` (a `print` in the _terminal_) of the content of the varialbes of the project loaded by `direnv`

## ⚙️ Run your first training locally

⚙️ We want you to check that you can run every "routes" in `taxifare.interface.main` _one by one_, to make sure your understand how your package works.

```python
if __name__ == '__main__':
    # preprocess()
    # preprocess(train_set)
    # train()
    # pred()
    # evaluate()
```

To do so, you can either:
- 🥵 Uncomment each route below one after the other, and run `python -m taxifare.interface.main` from your terminal
- 😇 or (smarter) use each of the following make commands we created for you! (check how they are written)

```bash
make run_preprocess
make run_train
make run_pred
make run_evaluate
make run_all
```

🏁 You are ready to go!

</details>
<br>

# 3️⃣ GCP SETUP

- Make sure that your machine is in the launch pad, ready to ignite the **Google Cloud Platform** 🛰
- **GCP** will allow you to allocate and use remote resources in the cloud

<details>
<summary markdown='span'><strong>❓Instructions (expand me)</strong></summary>

[//]: # ( challenge tech stack: gcloud gsutil cloud-storage )

[//]: # ( challenge presentation )

First things first, let's make sure that your machine is ready to drive **Google Cloud Platform** resources:
- Verify that your **GCP** setup is operationnal
- Discover the `gcloud` and `gsutil` **[Command Line Interface](https://en.wikipedia.org/wiki/Command-line_interface)** tools provided by GCP in order to drive resources in the cloud

[//]: # ( challenge instructions )

## GCP setup check

We need to install some useful _python_ packages to interact from your code with GCP APIs such as [Cloud Storage](https://cloud.google.com/storage/docs/apis) and [BigQuery](https://cloud.google.com/bigquery/docs/reference/rest):

``` bash
pip install google-cloud-storage "google-cloud-bigquery<3.0.0"
```

We will now verify that:
- The `gcloud` CLI tool has access to (is authorized to drive the resources of) your GCP account
- The _python_ code running on your machine has access to your GCP account

**🧪 In your terminal, run `make test_gcp_setup`**

## The `gcloud` CLI

Let's discover the first CLI tool allowing you to drive your GCP resources from the terminal.

**❓ How do you list your GCP projects ?**

Find the `gcloud` command allowing you to list your **GCP project id**.

**📝 Fill the `PROJECT` variable in the `.env` project configuration with the name of your GCP project**

**🧪 Run the tests with `make test_gcp_project`**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You can use the `-h` flag or the `--help` (more details) parameter in order to retrieve contextual help on the `gcloud` commands or sub commands (use `gcloud billing -h` to list the gcloud billing sub commands or `gcloud billing --help` for a more detailed help on the sub commands).

  👉 Pressing `q` is usually the way to exit the help if the command did not terminate itself, (`Ctrl + C` also works)

  Also note that running `gcloud` without arguments lists all the available sub commands by group.
</details>

## Cloud Storage and the `gsutil` CLI

The second CLI tool that you will use often allows you to deal with files stored on Cloud Storage within **buckets**.

**❓ How do you create a bucket ?**

Find the `gsutil` command allowing you to create a **bucket**.

**💻 Create a bucket in your GCP account**

Imagine you are working on a project on which several teams are collaborating. You need to be able to identify on which bucket to store your files.

**❓ How do you list the GCP buckets you have access to ?**

Find the `gsutil` command allowing you to retrieve the name of your **bucket**.

**📝 Fill the `BUCKET_NAME` variable in the `.env` project configuration**

**🧪 Run the tests with `make test_gcp_bucket`**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You can also use the [Cloud Storage console](https://console.cloud.google.com/storage/) in order create a bucket or list the existing buckets and their content.

  Do you see how much slower than the command line the GCP console (web interface) is ?
</details>

</details>
<br>

# 4️⃣ DATA IN THE CLOUD

- Discover how to upload data to **Big Query**
- Your package will be able to train incrementally from data in the cloud

<details>
  <summary markdown='span'><strong>❓Instructions (expand me)</strong></summary>


[//]: # ( challenge tech stack: big-query bq )

[//]: # ( challenge instructions )


## Build your first data warehouse

⚠️ The goal here is not to challenge your internet connection, so we will not have you wait while all your classmates simultaneously try to upload the 170GB of the _TaxiFare_ dataset to their own BigQuery dataset 🙌

Download the [sample 10k training dataset](https://storage.googleapis.com/datascience-mlops/taxi-fare-ny/train_10k.csv) and the [sample 10k validation dataset](https://storage.googleapis.com/datascience-mlops/taxi-fare-ny/val_10k.csv) on your machine and store them to `~/.lewagon/mlops/data` _if it has not been done yet_.

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

  There is a command for everything. You may use `curl` to download the data:

  ``` bash
  curl https://storage.googleapis.com/datascience-mlops/taxi-fare-ny/train_10k.csv > ~/.lewagon/mlops/data/train_10k.csv
  curl https://storage.googleapis.com/datascience-mlops/taxi-fare-ny/val_10k.csv > ~/.lewagon/mlops/data/val_10k.csv
  ```
</details>

Let's upload our sample 10k datasets CSV to **Big Query**.

**❓ How do you create a dataset in a data warehouse ?**

**💻 Find the `bq` command allowing you to create a new _dataset_. Create a dataset and add 2 new _tables_ `train_10k` and `val_10k` into the dataset, one for our training set and another for our validation set.**

**📝 Fill in the `DATASET` variable in the `.env` project configuration**

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

**🧪 Run the tests with `make test_big_query`**

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

Let's adapt the code of our package in order to source the data chunks used for the training from Big Query.
As explained previously, `data.py` acts as a switch.

- We already provided you with the code of the `data_sources.local_disk` _module_ so you can see how the `get_pandas_chunk` and `save_local_chunk` are working.
- Your role is to code the `data_sources.big_query` _module_ that contains `get_bq_chunk` and `save_bq_chunk` methods that you need to implement.

✋ Ask for a TA if you need explanations to understand any of the above steps.

**💻 Set the `DATA_SOURCE` variable in the `.env` file to `"big query"`. Complete the `get_bq_chunk` and `save_bq_chunk` functions in the `taxifare.data_sources.big_query` module. Add the required imports in `data.py`**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  If you look for *Paging through data table* in Big Query, or have a look at the [Big Query python API reference](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.client.Client.html), you should identify a method allowing you to retrieve the rows of a query one chunk after the next.
</details>

You can now train you model from the cloud using data chunks retrieved from Big Query 🎉

⚙️ **Train your model with data from Big Query**

- Run the following command: `python -m taxifare.interface.main` with DATA_SOURCE="big query".
- All main routes below should be working fine ✅

```python
if __name__ == '__main__':
    preprocess()
    train()
    pred()
    evaluate()
```

- Observe how the duration of the training varies when you source the data from Big Query versus when the data is stored on your machine. You can also time the result of your execution by prefixing `time <my_command>`

- 🧪 Run the tests with `make test_cloud_data`

🏁 Congrats! You have adapted your package to be able to source data incrementally in the cloud from either Cloud Storage or Big Query.

</details>
<br>


# 5️⃣ TRAIN IN THE CLOUD

Run the model training on a _virtual machine_ in the cloud using **Compute Engine**

<details>
  <summary markdown='span'><strong>❓Instructions (expand me)</strong></summary>


[//]: # ( challenge tech stack: compute-engine gcloud )

[//]: # ( challenge instructions )

## Enable the Compute Engine service

In GCP, many services are not enabled by default. The service to activate in order to use _virtual machines_ is **Compute Engine**.

**❓ How do you enable a GCP service ?**

Find the `gcloud` command allowing you to enable a **service**.

<details>
  <summary markdown='span'>💡 Hints</summary>

[Enabling API](https://cloud.google.com/endpoints/docs/openapi/enable-api#gcloud)
</details>

## Create your first Virtual Machine

The `taxifare` package is ready to train on a machine in the cloud. Let's create our first *Virtual Machine* instance!

**❓ Create a virtual machine**

Head towards the GCP console [Compute Engine](https://console.cloud.google.com/compute) page. The console will allow you to explore easilly the options available. Make sure to create an **Ubuntu** instance (read this _How to_, and have a look at the _Hint_).

<details>
  <summary markdown='span'><strong> 🗺 How to configure your VM instance </strong></summary>


  Let's explore the options available. The top right of the interface gives you a monthly estimate of the cost for the selected parameters if the VM remains on all the time.

  The basic options should be enough for what we want to do now, except for one: we want to choose the operating system that the VM instance will be running.

  Go to the *Boot disk* section, *CHANGE* the *Operating System* to **Ubuntu** and select the latest **Ubuntu xx.xx LTS** (Long Term Support) version.

  Ubuntu is the familly of operating systems that will ressemble the most the configuration on your machine following the [Le Wagon setup](https://github.com/lewagon/data-setup). Whether you are on a Mac, using Windows WSL2 or on Linux. Selecting this option will allow you to play with a remote machine using the commands you are already familiar with.
</details>

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

  In the future, when you know exactly what type of VM you want to create, you will be able to use the `gcloud compute instances` commands if you want to do everything from the command line. For example:

  ``` bash
  INSTANCE=taxi-instance
  IMAGE_PROJECT=ubuntu-os-cloud
  IMAGE_FAMILY=ubuntu-2204-lts

  gcloud compute instances create $INSTANCE --image-project=$IMAGE_PROJECT --image-family=$IMAGE_FAMILY
  ```
</details>

**💻 Fill the `INSTANCE` variable in the `.env` project configuration**


## Setup your VM

You have access at arms length to virtually unlimited computing power. Ready to help with trainings or any tasks.

**❓ How do you connect to the VM ?**

The GCP console allows you to connect to the VM instance through a web interface:

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-vm-ssh.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-vm-ssh.png" width="150" alt="gce vm ssh"></a><a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-console-ssh.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-console-ssh.png" width="120" alt="gce console ssh"></a>

You can disconnect by typing `exit` or closing the window.

A nice alternative is to connect to the virtual machine right from your command line 🤩

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-ssh.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-ssh.png" width="150" alt="gce ssh"></a>

All you need to do is to `gcloud compute ssh` on a running instance and to run `exit` when you want to disconnect 🎉

``` bash
INSTANCE=taxi-instance

gcloud compute ssh $INSTANCE
```

<details>
  <summary markdown='span'><strong> 💡 Error 22 </strong></summary>


  If you encounter a `port 22: Connection refused` error, just wait a little more for the VM instance to complete its startup.

  Just run `pwd` or `hostname` if you ever wonder on which machine you are running your commands.
</details>

**❓ How do you setup the VM to run your python code ?**

Let's run a light version of the [Le Wagon setup](https://github.com/lewagon/data-setup).

**💻 Connect to your VM instance and run the commands of the following sections**

<details>
  <summary markdown='span'><strong> ⚙️ <code>zsh</code> and <code>omz</code> (expand me)</strong></summary>

The **zsh** shell and its **Oh My Zsh** framework are the _command line interface_ configuration you are already familiar with. Accept to make zsh the default shell when prompted to.

``` bash
sudo apt update
sudo apt install -y zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

👉 Now the _cli_ of the remote machine starts to look a little more like the _cli_ of your local machine
</details>

<details>
  <summary markdown='span'><strong> ⚙️ <code>pyenv</code> and <code>pyenv-virtualenv</code> (expand me)</strong></summary>

Clone the `pyenv` and `pyenv-virtualenv` repos on the VM:

``` bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
```

Open ~/.zshrc in a Terminal code editor:

``` bash
nano ~/.zshrc
```

Add `pyenv`, `ssh-agent` and `direnv` to the list of `zsh` plugins in the line `plugins=(git)` in the `~/.zshrc`: you should have `plugins=(git pyenv ssh-agent direnv)`. Then exit and save (`Ctrl + X`, `Y`, `Enter`) and save:

Make sure that the modifications are saved:

``` bash
cat ~/.zshrc | grep "plugins="
```

Add the pyenv initialization script to your `~/.zprofile`:

``` bash
cat << EOF >> ~/.zprofile
export PYENV_ROOT="\$HOME/.pyenv"
export PATH="\$PYENV_ROOT/bin:\$PATH"
eval "\$(pyenv init --path)"
EOF
```

👉 Now we are ready to install python

</details>

<details>
  <summary markdown='span'><strong> ⚙️ <code>python</code> (expand me)</strong></summary>

Add dependencies required to build python:

``` bash
sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
python3-dev
```

ℹ️ If a window pops up to ask you which services to restart, just press *Enter*:

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-apt-services-restart.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-apt-services-restart.png" width="150" alt="gce apt services restart"></a>

Now we need to start a new user session so that the updates in the `~/.zshrc` and `~/.zprofile` are taken into account.

Exit the _virtual machine_: you need to `exit` from `zsh` (since you just installed it), then `exit` from the _vm_:

``` bash
exit
exit
```

Then reconnect:

``` bash
gcloud compute ssh $INSTANCE
```

Install python `3.8.12` and create a `lewagon` virtual env. This can take a while and look like it is stuck, but it is not:

``` bash
pyenv install 3.8.12
pyenv global 3.8.12
pyenv virtualenv 3.8.12 lewagon
pyenv global lewagon
```

</details>

<details>
  <summary markdown='span'><strong> ⚙️ <code>git</code> authentication to GitHub (expand me)</strong></summary>

Copy your private key 🔑 to the _vm_ in order to allow it to access to your GitHub account.

⚠️ Run this single command on your machine, not in the VM ⚠️

``` bash
INSTANCE=taxi-instance

# scp stands for secure copy (cp)
gcloud compute scp ~/.ssh/id_ed25519 $INSTANCE:~/.ssh/
```

If the command fails and ask for a user name, use the following variation:

``` bash
USER=toto

gcloud compute scp ~/.ssh/id_ed25519 $USER@$INSTANCE:~/.ssh/
```

⚠️ Then resume to running other commands in the VM ⚠️

Register the key you just copied:

``` bash
ssh-add ~/.ssh/id_ed25519
```

Enter your *passphrase* if asked to.

👉 You are now able to interact with your **GitHub** account from your the _virtual machine_
</details>

<details>
  <summary markdown='span'><strong> ⚙️ <em>python</em> code authentication to GCP (expand me)</strong></summary>

The code of your package needs to be able to access to your Big Query data warehouse.

In order to do so, we will copy your service account json key file 🔑 to the vm.

⚠️ Run this single command on your machine, not in the VM ⚠️

``` bash
INSTANCE=taxi-instance

gcloud compute scp $GOOGLE_APPLICATION_CREDENTIALS $INSTANCE:~/.ssh/
gcloud compute ssh $INSTANCE --command "echo 'export GOOGLE_APPLICATION_CREDENTIALS=~/.ssh/$(basename $GOOGLE_APPLICATION_CREDENTIALS)' >> ~/.zshrc"
```

If the command fails and ask for a user name, use the following variation:

``` bash
USER=toto

gcloud compute scp $GOOGLE_APPLICATION_CREDENTIALS $USER@$INSTANCE:~/.ssh/
gcloud compute ssh $INSTANCE --command "echo 'export GOOGLE_APPLICATION_CREDENTIALS=~/.ssh/$(basename $GOOGLE_APPLICATION_CREDENTIALS)' >> ~/.zshrc"
```

⚠️ Then resume to running other commands in the VM ⚠️

Reload your `~/.zshrc`:

``` bash
source ~/.zshrc
```

Let's verify that python code can now access your GCP resources. First install some packages:

``` bash
pip install google-cloud-storage
```

Then [run python code from the _cli_](https://stackoverflow.com/questions/3987041/run-function-from-the-command-line). This should list your GCP projects:

``` bash
python -c "from google.cloud import storage; \
    buckets = storage.Client().list_buckets(); \
    [print(b.name) for b in buckets]"
```

</details>

<details>
  <summary markdown='span'><strong> ⚙️ Make a generic data science setup (expand me)</strong></summary>

Install all the packages of the bootcamp on your VM:

``` bash
pip install -U pip
pip install -r https://raw.githubusercontent.com/lewagon/data-setup/master/specs/releases/linux.txt
```

</details>

Your _VM_ is now fully operational with:
- An environment (python + package dependencies) to run your code
- The credentials to connect to your _GitHub_ account
- The credentials to connect to your _GCP_ account

The only thing that is missing is the code of your project...

**🧪 Let's run a few tests inside your _VM terminal_ before we install it:**

- Default shell is `/usr/bin/zsh`
    ```bash
    echo $SHELL
    ```
- Python version is `3.8.12`
    ```bash
    python --version
    ```
- Active GCP project is the same as `$PROJECT` in your `.env` file
    ```bash
    gcloud config list project
    ```

Your VM is now a data science beast 🔥

## Train in the cloud

Let's run your first training in the cloud!

**❓ How do you setup and run your project in the virtual machine ?**

**💻 Clone your package, install its requirements**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

You can copy your code to the VM by cloning your GitHub project with this syntax:

Myriad batch:
```bash
git clone git@github.com:<user.github_nickname>/cloud-training
```

Legacy batch:
```bash
git clone git@github.com:<user.github_nickname>/data-challenges
```

Enter the directory of your package (adapt the command):

``` bash
cd <path/to/the/package/model/dir>
```

Create directories to save the model to:

``` bash
mkdir -p data
mkdir -p training_outputs/models
mkdir -p training_outputs/params
mkdir -p training_outputs/metrics
```

Create a `.env` file with all required parameters to drive your package:

``` bash
cp .env.sample .env
```

Fill the content of the `.env` (complete the missing values):

``` bash
nano .env
```

``` bash
DATA_SOURCE=big query
LOCAL_DATA_PATH=data
LOCAL_REGISTRY_PATH=training_outputs
```

Install `direnv` to load your `.env`:

``` bash
sudo apt update
sudo apt install -y direnv
```

ℹ️ If a window pops up to ask you which services to restart, just press *Enter*.

Disconnect from the _vm_ then reconnect (so that `direnv` works):

``` bash
exit
```

``` bash
gcloud compute ssh $INSTANCE
```

Allow your `.envrc`:

``` bash
direnv allow .
```

Remove the existing local environment:

``` bash
rm .python-version
```

Install the dependencies of the package:

``` bash
pip install pyarrow tensorflow  # this should be in your requirements.txt
pip install -r requirements.txt
```

</details>

**🔥 Run the preprocess and the training in the cloud 🔥**!

``` bash
make run_all  # Have a look at the Makefile to understand exactly what this does!
```

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-train-ssh.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-train-ssh.png" width="150" alt="gce train ssh"></a><a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-train-web-ssh.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-train-web-ssh.png" width="120" alt="gce train web ssh"></a>

**🏋🏽‍♂️ Go Big: re-run everything switching to 500k data sizes and 100k chunks 🏋🏽‍♂️**!


**🏁 Switch ON/OFF your VM to finish 🌒**

You can easily start and stop a vm instance from the GCP console, which allows to see which instances are running.

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-vm-start.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-vm-start.png" width="150" alt="gce vm start"></a>

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

A faster way to start and stop your virtual machine is to use the command line. The commands still take some time to complete, but you do not have to navigate through the GCP console interface.

Have a look at the `gcloud compute instances` commands in order to start, stop or list your instances:

``` bash
INSTANCE=taxi-instance

gcloud compute instances stop $INSTANCE
gcloud compute instances list
gcloud compute instances start $INSTANCE
```
</details>

🚨 Computing power does not grow on trees 🌳, do not forget to switch the VM off whenever you stop using it 💸

</details>
