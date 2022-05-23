
[//]: # ( presentation of the unit )

**🪐 Enter the dimension of Cloud Computing! 🚀**

In the previous unit, you have packaged the notebook of the `WagonCab` **Data Science** team. And you updated the code so that the model can be trained on the full `TaxiFare` dataset.

In this unit, you will learn how to grow from a **Data Scientist** into a **ML Engineer** 🤩

A **Data Scientist** does all their research work on a single machine, either their local machine or a machine in the cloud through a hosted service such as **Colab** for example.

A **ML Engineer** knows how to dispatch their work to several machines and use a pool of cloud ressources, remote storage or processing capacities, as their playground.

You will discover how to split your work into jobs dispatched to multiple machines in the cloud, so that manually trigerring the execution of your code is no longer a bottleneck for the model lifecycle.

You will learn how to drive a remote machine in a data center located anywhere in the world! Or in space if you find a cloud provider that offers capacity there 👽

The ressources of the cloud will be accessible literaly at your fingertips. Through the **Terminal** or through a **Graphical User Interface**.

[//]: # ( unit tech stack: gcloud gsutil cloud-storage compute-engine mlflow vertex-ai )

[//]: # ( presentation of the challenges of the unit )

## Unit challenges

**1️⃣ Project structure**
- Discover the structure of the challenges that you will be tackling for the rest of the module

**2️⃣ Environment**
- Setup the configuration for your project

**3️⃣ Setup check**
- Let's make sure that your machine is in the launch pad, ready to ignite **Google Cloud Platform** 🛰
- **GCP** will allow you to allocate and use remote ressources in the cloud

**4️⃣ Data in the cloud**
- We will upload our data to **Cloud Storage** and **Big Query**
- This will allow our package to train incrementally from data in the cloud

**5️⃣ Train in the cloud**
- The first job that we will dispatch to another machine is the model training
- We will use **Compute Engine** to allocate a VM for the training

**▶️ Recap - Vertex AI: training on a managed VM**
- Discover **Vertex AI Workbench** which allows us to train models in the cloud with minimal setup

[//]: # ( challenge tech stack: )

[//]: # ( challenge presentation )

In the remainder of the **MLOps** module, you will continue to work on the **WagonCab** project. Each new challenge will bring to the codebase an additional set of features on which to work.

In order to simplify your work, from now on, you will start from scratch on each challenge with the solution of the previous challenge. Let's discover our new playground!

🚨 Take the time to read throroughly the following in order to understand the structure of the code that you will be working with for the rest of the module and the new commands available.

In this challenge, we present the new structure of the project your will work with from now on.

[//]: # ( challenge instructions )

## Project structure

The structure the project that you discovered during the previous unit will remain the same from one challenge to the next. With a few twists that we will describe below. Here are the main files of interest:

``` bash
.                                                 # challenge root
└── model                                         # `taxifare-model` package
    ├── .python-version                           # 🐍 virtual env choice
    ├── Makefile                                  # 🐚 make commands
    ├── requirements.txt
    ├── setup.py
    └── taxifare_model
        ├── data_sources
        │   └── local_disk.py                     # 🚚 data exchange functions
        ├── interface
        │   └── main.py                           # 🚪 entry point
        └── ml_logic
            ├── data.py                           # 📦 data storage interface
            ├── params.py
            ├── registry.py                       # 📦 model storage interface
            └── utils.py
```

At the moment, the project only contains a `model` directory for our `taxifare-model` package.

The `model` directory is the location at which you will spend most of the time. From this directory, you will run your `python -m` or `Makefile` commands.

### 🐍 `.python-version`

We want to work with a dedicated `taxifare-model` virtual environment for our `taxifare-model` package. This file ensures that any python command ran in the `model` directory is executed within the `taxifare-model` virtual environment.

Beware, when stepping up from the `model` directory (`cd ..` or `cd ~`), you will resume to the gloval `lewagon` virtual environment (the packages installed will not be the same).

### 🐚 `Makefile`

You have already used commands to test your challenges in the last unit.

From now on you will use a different set of commands:
- `make list` lists the available commands (try it now 🤩, more commands will be added in the units to come)
- `make show_env` will produce an empty output for now (you will start to use it on the next challenges)
- `make run_model` runs the `taxifare_model` package (basically a `python -m taxifare_model.interface.main`)
- `make reinstall_package` installs the package of the current challenge in the virtual environment (🚨 you do not want to call the package of the previous challenge by mistake when running your code or a `Makefile` command)
- `make dev_test` allows you to run the tests ✅

<details>
  <summary markdown='span'><strong> 💡 How to run these commands ? </strong></summary>


  The `make` commands must be ran in the directory containing the `Makefile`. In order to run them you should be in the `model` directory:

  ``` bash
  cd ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/02-Cloud-training/02-Project-structure/model
  ```
</details>

### 🚪 `main.py`

Bye bye `taxifare_model.interface.main_local` module, you served us well ❤️

Long live `taxifare_model.interface.main`, our new package entry point ⭐️

`main.py` works the same way as `main_local` did, and has the following functions:

- `preprocess_and_train`: preprocess and train data in one go
- `preprocess`: preprocess data by chunk
- `train`: train data by chunk
- `evaluate`: evaluate the performance of the latest trained model on new data
- `pred`: make a prediction on a `DataFrame` with a specific version of the trained model

🚨 One main change in the code of the package is that we choose to have it delegate some of its work to dedicated modules in order to limit the size of the principal files.

The code of the model, the preprocessing and the data cleaning does not change: we are still working on the same content from the WagonCab Data Science team!

The main changes are:
- The way we source the project configuration (we want a single configuration for all the challenges)
- The way we source the training data (we want a single local data source for all the challenges - and other data sources in the cloud later on)
- The way we stored the trained model (we want to be able to store our trained model locally - or °_spoiler alert_° in the cloud)

### First delegation: 📦 `data.py` + 🚚 `local_disk.py`

`data.py` used to be only responsible for data cleaning (with `clean_data`), and `main_local.py` used to `pd.read_csv` in order to retrieve the data.

Now, the code of the project follows the principle of [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns): `main.py` does not need to know where the data comes from, or with which function or package it was read. It just wants to ask some piece of code to provide the data it asks for.

The role of `main.py` is to ask for data to `data.py`, without having to know what is going on behind the scenes. `main.py` then delegates the training logic to `model.py`. We described roles and delegation for files because they bundle our code in this project, but delegation is more often referred to when talking about **classes** whose job it is to encapsulate state and behavior.

Similarly to how `main.py` deletages data retrieval to `data.py`, `data.py` in its turn delegates the job of `pd.read_csv` to `local_disk.py`.

<details>
  <summary markdown='span'><strong> 💡 Why did we do that ? </strong></summary>


  The job of `data.py` is not to actually read the data. But to ask someone else (`local_disk.py`) to do it.

  👉 This separation is an indication that in the challenges to come we might want to retrieve data from other sources (who said *Cloud Storage* and *Big Query* ?)
</details>

👉 Splitting the responsabilities of your code into smaller *files*, *functions* (or even *classes*) allows to [keep things simple](https://en.wikipedia.org/wiki/KISS_principle). This allows you to concentrate on a small piece of code without having to worry about everything else that is going on anywhere else in the project 🧶 The larger your project grows, the more impact separation of responsibilities has

Delegation is a rule of thumb, the organisation of the code is highly sensitive to the culture of the teams and the preferences of the individuals 🙌

Similarly, 📦 `registry.py` will grow in the coming units when we decide to save our trained model to the cloud.

### Second delegation: the ⚙️ `.env` **project configuration**

The project will follow the principle of _separation of configuration from code_ and load the configuration for its behavior from _environment variables_.

For example the code will use the `DATASET_SIZE` environment variable in order to determine the size of the dataset on which to work.

Previously the `DATASET_SIZE` variable was stored in `params.py`. It has moved with his configuration friends to the `.env` project configuration... More on that in the next challenge !

You are going to play with a dozen parameters throughout the challenges in order to determine which **GCP** project to work with, select the data sources to retrieve data from, define your secrets and credentials, fill the coordinates of the third party services your project will be using, and so on.

Nobody wants to copy paste the project configuration from one challenge to the next 😬

Remember that these settings are personal and contain sensitive data 🔑 that must not be stored in **git**.

The way to respond to this issue is to have the project retrieve its parameters from the [environment](https://stackoverflow.com/questions/4906977/how-do-i-access-environment-variables-in-python) and to store the parameters in a `.env` project configuration file that is referenced in the `.gitignore` file so that it cannot be committed.

Being able to configure the behavior of the package without having to update hard-coded values in the code will be very useful when we decide to put the project in production 🚀

## Challenges, **project parameters** and **local data storage**

Last change in the project: we do not want to copy paste our dataset from one challenge to the next.

We will move the data to the `~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/data` directory.

Here is the target structure of the `<program.challenges_repo_name>` repository:

``` bash
~                                                 # 🏠 your home
└── code
    └── <user.github_nickname>
        └── <program.challenges_repo_name>
            ├── .git                              # 🕰 the git directory storing the commits for the changes in `<program.challenges_repo_name>`
            └── 07-ML-Ops
                ├── 01-Train-at-scale             # ✅ check!
                ├── 02-Cloud-training
                │   ├── 01-Shell-practice         # 👊 done that too!
                │   ├── 02-Structure              # 🎯 you are here
                │   ├── 03-Environment
                │   ├── 04-Setup-check
                │   ├── 05-Store-data-in-the-cloud
                │   ├── 06-Train-in-the-cloud
                │   └── 07-Predict-in-the-cloud
                ├── 03-Automate-model-lifecycle
                ├── 04-Predict-in-production
                ├── 05-User-interface
                ├── .env                          # ⚙️ global project parameters
                ├── .envrc                        # 🎬 .env loader (used by `direnv`)
                ├── data                          # 📦 local data storage
                ├── notebooks                     # 🔬 data science is going on here
                └── registry                      # 🧬 trained models
```

**💻 Let's create a data directory which will be sourced by all the challenges to come**

``` bash
mkdir ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/data
cd ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/data
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_1k.csv > raw/train_1k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_10k.csv > raw/train_10k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_100k.csv > raw/train_100k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/val_1k.csv > raw/val_1k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/val_10k.csv > raw/val_10k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/val_100k.csv > raw/val_100k.csv
```

**💻 We will copy the notebooks as well to a central location right next to the data directory**

``` bash
cd ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops
cp -R ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/01-Train-at-scale/01-Train-at-scale/model/notebooks .
```

**💻 Then create a centralized local registry directory for our trained models**

``` bash
mkdir ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/registry
mkdir ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/registry/metrics
mkdir ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/registry/models
mkdir ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/registry/params
```

**💻 Run the verification command**

``` bash
cd ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/data
ls -tRalala . > ../02-Cloud-training/02-Project-structure/model/tests/structure/test_structure_data.txt
```

Go back to the project directory

``` bash
cd ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/02-Cloud-training/02-Project-structure/model
```

**🧪 Run the tests with `make dev_test`**

👉 `test_structure_data` should be ✅

🏁 Congrats! That was a lot of reading, call a TA if you have any questions, it is important to be confident with what is going on here.
