
[//]: # ( challenge tech stack: )

**💻 Install the package of the current challenge with `make reinstall_package`**

**💻 Do not forget to handle your `.env` file (_copy_ the `.env.sample`, _fill_ the `.env`, _allow_ `direnv`)**

[//]: # ( challenge instructions )

You have completed your work on the `taxifare` package. You have transformed the notebook provided by the WagonCab Data Science team into a cloud ready package. Your code is able to train from various data sources (your local disk, Cloud Storage or Big Query) depending on the value of the `.env` variable `DATA_SOURCE`. The code can also save the trained model on your local disk or in mlflow depending on the value of the `MODEL_TARGET` environment variable.

The WagonCab tech team is amazed by your work and decides to assign to you a new challenging task: automating the complete workflow of the model lifecycle.

The team wants to value your time as much as possible and tasked an itern to provide you with the **Prefect** boilerplate code for a new package that will allow you to automate the complete lifecycle of your model 🤩

## Workflow package structure

Here are the new files added by the intern:

``` bash
.
└── model
    ├── .python-version
    ├── Makefile
    ├── requirements.txt
    ├── setup.py
    ├── flow
    │   ├── flow.py                               # ♻️ workflow lifecycle code
    │   └── main.py                               # 🚀 workflow launcher
    ├── data_sources
    │   ├── big_query.py
    │   └── local_disk.py
    ├── interface
    │   └── main.py
    └── ml_logic
        ├── data.py
        ├── encoders.py
        ├── model.py
        ├── params.py
        ├── preprocessor.py
        ├── registry.py
        ├── registry_db.py                    # 📦 mlflow database interface
        └── utils.py
```

The new code is still located inside of the `taxifare` package because it is so tightly coupled with the code that handles the model training that it would not make sense to separate both in different packages.

You will still be able to play with the new code and the existing one from the `model` directory.

### `flow.py`

The trainee provided you with a full **Prefect** workflow boilerplate that they think will best allow you to plug the `taxifare` package and build a complete automation for its lifecycle.

The new intern of the company is a little bit clumbsy and might have forgotten a few imports 😬

Luckily for us, the [Prefect doc](https://docs.prefect.io/orchestration/) is awesome !

### `main.py`

The intern provided an entry point allowing you to trigger **ONE** run of the model lifecycle.

They also added a new `Makefile` _directive_ callable with `make run_flow`.

Each time you run `make run_flow` the `taxifare.flow.main` module is ran once, triggering a single full lifecycle of training for your model.

### `registry_db.py`

In all its wisdom, the intern thought it would be a good idea to have a function reponsible for querying the **mlflow** database in order to retrieve the latest row on which the model has trained.

This way whenever a new model lifecycle is ran the model only runs on the new data and does not retrain on data it has already seen.

## Configure your project for Prefect

❓ **What parameters do you need to interact with Prefect ?**

Edit your `.env` project configuration file and set the `PREFECT_FLOW_NAME` parameter. Pick a value that accurately describes what the workflow does (you can follow the `taxifare_lifecycle_<user.github_nickname>` convention or pick an exotic name).

Also create environment variables for `PREFECT_BACKEND` set to `local`. Playing with this variable in the future will allow your code to plug to an online **Prefect** server. Also set the `PREFECT_LOG_LEVEL` variable to `WARNING`. It allows you to retrieve more info on what prefect is doing behind the scenes (more info [here](https://docs.prefect.io/core/concepts/logging.html)).

**📝 Fill the `PREFECT_FLOW_NAME`, `PREFECT_BACKEND` and `PREFECT_LOG_LEVEL` variables in the `.env` project configuration**

**🧪 Run the tests with `make dev_test`**

👉 `test_prefect_parameters` should be ✅

## Complete the workflow

Lets assume you have installed prefect on your machine (or have a look at the latest version of the `requirements.txt` and install it).

❓ **How do you complete the workflow ?**

Our goal is to be able to run the workflow in an automated way, that is without any human supervision in the loop.

We want our worflow to:
- Look for new data push by the Data Engineer of the WagonCab team in our database (the data eng will always push new data in our data source training table)
- Evaluate the performance of our current model in _Production_ (remember the mlflow stage ?) on the new data
- Train the latest model in _Production_ with the new data an see how the performance improves
- Communicate to the team the performance of the past and new models on the new data in order to decide whether to put the newly trained model in _Production_

Luckily for us, all the features are already backed in our existing `taxifare` package, so we only have to do the wiring and make sure that everything works correctly !

**💻 Complete the `taxifare.flow.main` and all the functions in the `taxifare.flow.flow` module (look for `# YOUR CODE HERE`)**

**🧪 Run the tests with `make dev_test`**

👉 `test_prefect_flow` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You do not need to write all the code right away before you test it: just put fake values in the return of the functions that you have not finished yet and observe what happens when you `make run_flow`.
</details>

🏁 Congrats! You plugged the `taxifare` to a full workflow lifecycle
