
[//]: # ( presentation of the unit )

**🪐 Enter the dimension of Cloud Computing! 🚀**

In the previous unit, you have **packaged** 📦 the notebook of the _WagonCab_ data science team. And you updated the code so that the model can be trained on the _TaxiFare_ **full dataset** 🗻.

In this unit, you will learn how to grow from a **Data Scientist** into a **ML Engineer** 🤩

A _Data Scientist_ does all their research work on a single machine, either their local machine or a machine in the cloud through a hosted service such as **Colab** for example.

A _ML Engineer_ knows how to dispatch their work to several machines and use a pool of **cloud resources**, remote storage or processing capacities, as their playground.

You will discover how to split your work into jobs executed on multiple machines in the cloud, so that manually trigerring the execution of your code is no longer a bottleneck for the model lifecycle.

You will learn how to drive a remote machine in a data center located anywhere in the world! Or in space if you find a cloud provider that offers capacity there 👽

The resources of the cloud will be accessible at your fingertips, through a _Graphical User Interface_ for exploration using the **[web console 🌍](https://console.cloud.google.com/)**, through a **[terminal](https://en.wikipedia.org/wiki/Terminal_emulator)** 💻 to gain speed and efficiency, or through **code** 📝 when you want to automate your work.

[//]: # ( unit tech stack: gcloud gsutil cloud-storage compute-engine mlflow vertex-ai )

[//]: # ( presentation of the challenges of the unit )

## Unit challenges

**1️⃣ Project structure**
- Discover the file and directory **structure** of the challenges that you will be tackling for the rest of the module

**2️⃣ Environment**
- Learn how to setup the **application parameters** for your challenges

**3️⃣ Setup check**
- Make sure that your machine is in the launch pad, ready to ignite the **Google Cloud Platform** 🛰
- **GCP** will allow you to allocate and use remote resources in the cloud

**4️⃣ Data in the cloud**
- Discover how to upload data to **Cloud Storage** and **Big Query**
- Your package will be able to train incrementally from data in the cloud

**5️⃣ Train in the cloud**
- Run the model training on a _virtual machine_ in the cloud using **Compute Engine**

**▶️ Recap - Managed VM**
- Discover **Vertex AI Workbench** which allows to train models in the cloud with minimal setup

[//]: # ( challenge tech stack: )

[//]: # ( challenge presentation )

🚨 In the remainder of the **MLOps** module, all the challenges will have the same structure and base content. Each new challenge will bring an additional set of features on which to work

👉 From now on, you will start each new challenge with the solution of the previous challenge

❓ Now, read carefully the following document to discover the structure of the challenges

[//]: # ( challenge instructions )

## Project structure

The structure of the project that you discovered during the previous unit will remain the same in the next challenges. With a few twists described below. Here are the main files of interest:

``` bash
.                                                 # challenge root
├── Makefile
├── README.md
└── model
    ├── .env                                      # ⚙️ global project parameters (does not exist yet)
    ├── .env.sample                               # ⚙️ sample `.env` file containing the variables used in the challenge
    ├── .envrc                                    # 🎬 .env loader (used by `direnv`)
    ├── .gitignore
    ├── .python-version                           # 🐍 virtual env choice
    ├── Makefile                                  # 🐚 make commands
    ├── README.md
    ├── pytest.ini
    ├── requirements.txt
    ├── setup.py
    ├── taxifare_model
    │   ├── __init__.py
    │   ├── data_sources
    │   │   ├── __init__.py
    │   │   └── local_disk.py                     # 🚚 data exchange functions
    │   ├── interface
    │   │   ├── __init__.py
    │   │   └── main.py                           # 🚪 (new) entry point
    │   └── ml_logic
    │       ├── __init__.py
    │       ├── data.py                           # 📦 data storage interface (updated)
    │       ├── encoders.py
    │       ├── model.py
    │       ├── params.py
    │       ├── preprocessor.py
    │       ├── registry.py                       # 📦 model storage functions (updated)
    │       └── utils.py
    └── tests
```

As in the previous unit, you will spend most of your time in the `model` directory to run `python -m` or `make` commands.

### ⚙️ `.env.sample`

This file is a _template_ allowing you to create the `.env` file for each challenge. The `.env.sample` file contains the variables required by the code and expected in the `.env` file.

At the start of each challenge, you will need to:
1. **Copy** the content of the `.env.sample` file into a new `.env` file in the `model` directory
2. **Replace** the values of the variables in the `.env` file in order to define the context of execution for your code (anything that is specific to your machine or any of your credentials that the code requires)
3. **Allow** `direnv` to load the content of the `.envrc` (which in turn loads the variables of the `.env` file into the environment for the code to consume)

🚨 Keep in mind that the `.env` file **should never be stored in Git**. This is why we provide a git controlled `.env.sample` file that you must turn into a `.env` file before it is filled with sensitive data. The `.env` itself is listed in the `.gitignore` file in order to prevent its tracking by git

### 🐍 `.python-version`

This file specifies the virtual environment in which the code of the application runs: `taxifare-model`. Using a dedicated virtual environment with its dependencies listed in the `requirements.txt` allows us to ensure that the application continues to work as expected when deployed to production.

Beware, when stepping up from the `model` directory in which the `.python-version` sits (`cd ..` or `cd ~`), you will resume to the global `lewagon` virtual environment

### 🐚 `Makefile`

You are now already familiar with the `make` commands that you used in the previous challenges to test your code.

In the remainder of the module, the `Makefile` will contain dedicated commands allowing you to drive your package. Some challenges even come with dedicated commands to drive your resources.

Here are some of the new commands brought by this module in the `Makefile` of your challenges:
- `make list` lists the available `Makefile` commands (try it now 🤩, more commands will be added in the units to come)

```bash
make list
```

👉 You will see a `direnv` error in the terminal when you `cd` into the `model` directory because the `.env` file does not exist yet

- `make reinstall_package` installs the package of the current challenge in the virtual environment (🚨 you do not want to call the package of the previous challenge by mistake when running your code or a `Makefile` command). You do not need it now

The other commands listed by `make list` will not be working for the moment:
- `make show_env` lists the environment variables loaded by `direnv`. It will be empty for now since the `.env` file is empty
- `make run_model` runs the `taxifare_model` package (it runs `python -m taxifare_model.interface.main`). It will fail at the moment, since you have not configured the `.env` file yet
- `make dev_test` allows you to run the tests ✅ (for now it will fail as well since you have not completed the challenge yet 😉)

<details>
  <summary markdown='span'><strong> 💡 Are the commands not found ? </strong></summary>


  Whenever running a `make` command, make sure that you sit in the `model` directory (the `Makefile` at the root of the challenge does not contain the commands that you use)
</details>

### 🚪 `main.py`

Bye bye `taxifare_model.interface.main_local` module, you served us well ❤️

Long live `taxifare_model.interface.main`, our new package entry point ⭐️

`main.py` works the same way as `main_local` did, and has the following functions:

- `preprocess_and_train`: preprocess and train the data in one go
- `preprocess`: preprocess the data by chunk
- `train`: train the data by chunk
- `evaluate`: evaluate the performance of the latest trained model on new data
- `pred`: make a prediction on a `DataFrame` with a specific version of the trained model

🚨 One main change in the code of the package is that we choose to delegate some of its work to dedicated modules in order to limit the size of the `main.py` file. Simply put, the code structure changed a little and some _functions_ moved around

The code of the model, the preprocessing and the data cleaning files does not change 👌

The main changes concern:
- The project configuration: the code loads the application configuration from the environment variables loaded by `direnv` from the `.env` file
- The training data: the code uses the `data.py` module as an _interface_ to other modules that load the data either from a local data source or from the cloud depending on the `.env` configuration
- The model storage: the code evolves to store the trained model either locally - or °_spoiler alert_° in the cloud

### Data delegation: 📦 `data.py` + 🚚 `local_disk.py`

In the previous version of the code, the `data.py` module used to be only responsible for cleaning the data using `clean_data`. And the `main_local.py` module, the package entry point, would call `pd.read_csv` directly in order to load the data from disk. This means that the package entry point needed to know both where to load the data from (here the local disk) and with which package or framework to do it (here `pandas`). This type of code is pretty imbricated and complicated to update and maintain in the long term because every module touches every feature of the code. In the new version of the code, the project follows the principle of [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns): we want the `main.py` package entry point to be agnostic of the details and packages or frameworks used in order to retrieve the data, and to only concentrate on the flow control of our code (which modules to call and in what order). Each module will be responsible for fulfilling only its role. The less each module is aware of how other modules work, the easier it is to maintain and update our code in the long run, or to onboard new team members for that matter.

So, `main.py` does not need to know where the data comes from (local or cloud), or with which package or framework it was loaded. It just wants to call some module in order to retrieve the data it requires, without having to know anything about the job that is being done (if possible).

The role of `main.py` is to ask for data from `data.py`, without having to know what is going on behind the scenes. `main.py` then delegates the training logic to `model.py`. We described roles and delegation for files because they bundle our code in this project, but delegation is more often referred to when talking about _classes_ whose job it is to encapsulate the state and behavior of elements of your application.

Similarly to how `main.py` delegates data retrieval to `data.py`, `data.py` in its turn delegates to `local_disk.py` the work of reading data with `pd.read_csv`.

<details>
  <summary markdown='span'><strong> 💡 Why does `data.py` delegate its work to a single file in the first place ? </strong></summary>

  We could argue that `data.py` and `local_disk.py` could easily be merged.

  👉 This separation is an indication that in the challenges to come we might want to retrieve data from other data sources such as **Cloud Storage** or **Big Query**
</details>

👉 Splitting the responsabilities of your code into smaller *files*, *functions* (or even *classes*) allows to [keep things simple](https://en.wikipedia.org/wiki/KISS_principle). When working on a piece of code, it allows you to concentrate only on the code and its context without having to worry about how the rest of the project works 🧶

Delegation is a rule of thumb, the organisation of the code is highly sensitive to the culture of the teams and the preferences of the individuals 🙌

### Parameters delegation: the ⚙️ `.env` **project configuration**

The new version of the code follows the principle of [separation of configuration from code](https://12factor.net/config) and loads the configuration for its behavior from _environment variables_.

As an example, the code uses the `DATASET_SIZE` environment variable in order to determine the size of the dataset on which to work.

Previously the `DATASET_SIZE` variable was stored in `params.py`. It will move along with the other configuration variables to the `.env` project configuration file...

You are going to play with a dozen of parameters throughout the challenges in order to determine which **GCP** resources to work with, select the data sources to retrieve data from, define your secrets and credentials, fill the coordinates of the third party services your project will be using, and so on.

Remember (again) that these settings are personal and contain sensitive data 🔑 that must not be stored in **git**.

The way to respond to this issue is to have the project retrieve its parameters from the [environment](https://stackoverflow.com/questions/4906977/how-do-i-access-environment-variables-in-python) and to store the parameters in a `.env` project configuration file that is referenced in the `.gitignore` file so that it cannot be committed.

Being able to configure the behavior of the package without having to update hard-coded values in the code will be very useful when we decide to put the project in production 🚀

## Shared directories

Last change in the project: we do not want to copy paste our dataset from one challenge to the next.

We will move the `data`, `notebooks` and `training_outputs` directories to a centralised `~/.lewagon/mlops/` directory to be used by the coming challenges.

**💻 Let's move the data**

``` bash
mkdir -p ~/.lewagon/mlops/notebooks
mkdir -p ~/.lewagon/mlops/training_outputs
mv ~/code/<user.github_nickname>/{{local_path_to("07-ML-Ops/01-Train-at-scale/01-Train-at-scale")}}/model/data ~/.lewagon/mlops
```

You can now see that the data for the challenges to come is stored in `~/.lewagon/mlops/` along with the notebooks of the data science team and the model outputs:

``` bash
tree -a ~/.lewagon/mlops/
```

👉 Which will come in handy when you want to make some space and clean your model outputs 🧹

**💻 Run the verification command**

``` bash
cd ~/code/<user.github_nickname>/{{local_path_to("07-ML-Ops/02-Cloud-training/02-Project-structure")}}/model
ls -tRal ~/.lewagon/mlops/data > tests/structure/test_structure_data.txt
```

**💻 Install the package of the challenge with the `make reinstall_package` command**

**🧪 Run the tests with `make dev_test`**

👉 `test_package_version` and `test_structure_data` should be ✅

🏁 Congrats! That was a lot of reading, call a TA if you have any questions, it is important to be confident with what is going on here
