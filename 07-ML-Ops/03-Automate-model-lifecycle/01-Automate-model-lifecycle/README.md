
[//]: # ( presentation of the unit )

**🥁 Discover model lifecycle automation and orchestration 🎻**

In this unit, you will learn how to orchestrate and automate the lifecycle of your model.

You will see how to formalise the structure of the model lifecycle broken down into a set of tasks and how to organise these tasks together.

You will create an automated workflow for the **taxifare** 🚕 model that periodically runs the whole model lifecycle on remote machines in order to consume the new data that is regularly injected into your data source.

You will store monitoring data 🔎 to ensure that your model continues to perform correctly while you are away 🏝

## 1️⃣ Performance monitoring

- Use **mlflow** to store the trained models and the result of our experiments in the cloud
- Monitor the evolution of the performance of our models on new data over time

<details>
  <summary markdown='span'><strong>❓ Instructions (expand me)</strong></summary>

[//]: # ( challenge tech stack: mlflow )

**💻 Install the package of the current challenge with `make reinstall_package`**

**💻 Do not forget to handle your `.env` file (_copy_ the `.env.sample`, _fill_ the `.env`, _allow_ `direnv`)**

[//]: # ( challenge instructions )

### Configure your project for mlflow

First let's install the [psycopg](https://www.psycopg.org/) package required in order to connect to the mlflow database.

``` bash
pip install psycopg2-binary
```

The **WagonCab** tech team put in production a **mlflow** server located at https://mlflow.lewagon.ai. This will be useful in order to track your experiments and store your trained models.

We added a new `MODEL_TARGET` variable to the `.env` project configuration file. This variable defines how the `taxifare-model` package should save the _outputs of the training_ (i.e. the trained _model_, the training _parameters_ and _metrics_) once the training is ov.er. `MODEL_TARGET` can take 2 values: `local` or `mlflow`

❓ **What parameters do you need to interact with mlflow ?**

**📝 Edit your `.env` project configuration file:**

- `MODEL_TARGET` with the corresponding value
- `MLFLOW_EXPERIMENT` should contain `taxifare_experiment_<user.github_nickname>`
- `MLFLOW_MODEL_NAME` should contain `taxifare_<user.github_nickname>`

**🧪 Run the tests with `make test_mlflow_config`**

### Push your parameters

❓ **How do you push your training parameters to mlflow ?**

Let's update the code to push the experiment parameters to mlflow once the training it done.

The pushed params can include `learning_rate`, `batch_size`, and `context`. The code in the `taxifare.interface.main` module already pushes these for you thanks to the `taxifare.ml_logic.registry.save_model()` function:

```python
# main.py
def preprocess()
    #[...]
    # save params
    params = dict(
        # package behavior
        context="preprocess",
        chunk_size=CHUNK_SIZE,
        # data source
        first_row=first_row,
        row_count=row_count,
        cleaned_row_count=cleaned_row_count)

    save_model(params=params)
```

**💻 Complete the first step of the `save_model` function in the `taxifare.ml_logic.registry` module**

```python
# registry.py
def save_model(model: Model = None,
               params: dict = None,
               metrics: dict = None) -> None:
    """
    persist trained model, params and metrics
    """

    if os.environ.get("MODEL_TARGET") == "mlflow":

        print(Fore.BLUE + "\nSave model to mlflow..." + Style.RESET_ALL)

        # retrieve mlflow env params
        # YOUR CODE HERE

        with mlflow.start_run():

            # push parameters to mlflow
            # YOUR CODE HERE
```

**💻 Try to run a training using `make run_model`**

**✅ Check on the mlflow interface if your parameters has been pushed**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

  Have a look at the [mlflow python API documentation](https://mlflow.org/docs/latest/python_api/mlflow.html).

  Do not forget to set the tracking server with `mlflow.set_tracking_uri` and to provide an experiment name with `mlflow.set_experiment`.
</details>

### Push your metrics

❓ **How do you push your training metrics to mlflow ?**

Let's now push the metrics to mlflow. The code should be almost the same as for the parameters of the experiment.

The pushed metrics can include `val_mae`, `mean_val` and `mae`. Again, it is already handled in the `taxifare.interface.main` module:

```python
# main.py
def evaluate()
    #[...]
    metrics_dict = evaluate_model(model=model, X=X_new_processed, y=y_new)
    #[...]
    save_model(params=params, metrics=metrics_dict)
```

**💻 Complete the second step of the `save_model` function in the `taxifare.ml_logic.registry` module**

```python
# registry.py
def save_model(model: Model = None,
               params: dict = None,
               metrics: dict = None) -> None:
    """
    persist trained model, params and metrics
    """

    if os.environ.get("MODEL_TARGET") == "mlflow":
        #[...]
        with mlflow.start_run():
            # STEP 1: push parameters to mlflow
            #[...]

            # STEP 2: push metrics to mlflow
            # YOUR CODE HERE
```

**💻 Try to run a training using `make run_model`**

**✅ Check your metrics has been pushed to mlflow**

### Push your trained model

❓ **How do you push your trained model to mlflow ?**

Now for the better part: mlflow allows us to store the trained model so that we can easily refer to it when we want to make a prediction.

This will allow you colleagues to use smoothly the model you have trained !

**💻 Complete the third step of the `save_model` function in the `taxifare.ml_logic.registry` module**

```python
# registry.py
def save_model(model: Model = None,
               params: dict = None,
               metrics: dict = None) -> None:
    """
    persist trained model, params and metrics
    """

    if os.environ.get("MODEL_TARGET") == "mlflow":
        #[...]
        with mlflow.start_run():
            # STEP 1: push parameters to mlflow
            #[...]

            # STEP 2: push metrics to mlflow
            # [...]

            # STEP 3: push model to mlflow
            # YOUR CODE HERE
```

**💻 Try to run a training using `make run_model`**

**✅ Check your model has been pushed to mlflow**

**💻 Put your model in Production in the mlflow UI**

<details>
  <summary markdown='span'><strong> 💡 Hint</strong></summary>

  Have a look at the [mlflow python API for Keras](https://mlflow.org/docs/latest/python_api/mlflow.keras.html) and find a function allowing you to upload your trained model.
</details>

### Make a prediction from you model saved in mlflow

What use is it to store my model in mlflow you say ? Well for starters mlflow allows you to handle very easily the lifecycle stage (_None_, _Staging_ or _Production_) of the model in order to synchronize the information accross the team. And more importantly, it allows any application to load a trained model in a given stage in order to make a prediction.

❓ **How do you make a prediction from a trained model stored in mlflow ?**

**💻 Complete the `load_model` function in the `taxifare.ml_logic.registry` module, then run a training using `make run_model`**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

  Have a look at the [mlflow python API for Keras](https://mlflow.org/docs/latest/python_api/mlflow.keras.html) and find a function allowing you to retrieve your trained model.
</details>

🏁 Congrats! Your `taxifare` package is now persisting every aspect of your experiments in **mlflow**

</details>

## 2️⃣ Automated model lifecycle

- We will build a workflow to retrain periodically the model with fresh data and monitor the performance of the new model
- But always keep a human 👀 in the loop

<details>
  <summary markdown='span'><strong>❓ Instructions (expand me)</strong></summary>

The WagonCab tech team is amazed by your work and decides to assign to you a new challenging task: automating the complete workflow of the model lifecycle.

The team wants to value your time as much as possible and tasked an itern to provide you with the **Prefect** boilerplate code for a new package that will allow you to automate the complete lifecycle of your model 🤩

### Workflow package structure

Here are the new files added by the intern:

``` bash
.
└── taxifare
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

#### `taxifare.flow.flow.py`

The trainee provided you with a full **Prefect** workflow boilerplate that they think will best allow you to plug the `taxifare` and build a complete automation for its lifecycle.

The new intern of the company is a little bit clumbsy and might have forgotten a few imports 😬

Luckily for us, the [Prefect doc](https://docs.prefect.io/orchestration/) is awesome !

#### `taxifare.flow.main.py`

The intern provided an entry point allowing you to trigger **ONE** run of the model lifecycle.

They also added a new `Makefile` _directive_ callable with `make run_flow`.

Each time you run `make run_flow` the `taxifare.flow.main` module is ran once, triggering a single full lifecycle of training for your model.

#### `taxifare.ml_logic.registry_db.py`

In all its wisdom, the intern thought it would be a good idea to have a function reponsible for querying the **mlflow** database in order to retrieve the latest row on which the model has trained.

This way whenever a new model lifecycle is ran the model only runs on the new data and does not retrain on data it has already seen.

### Configure your project for Prefect

❓ **What parameters do you need to interact with Prefect ?**

**📝 Edit your `.env` project configuration file:**
- `PREFECT_FLOW_NAME` should follow `taxifare_lifecycle_<user.github_nickname>` convention
- `PREFECT_LOG_LEVEL` variable to `WARNING`(more info [here](https://docs.prefect.io/core/concepts/logging.html)).

**🧪 Run the tests with `make test_prefect_config`**

### Complete the workflow

❓ **How do you complete the workflow ?**

Our goal is to be able to run the workflow in an automated way, that is without any human supervision in the loop.

We want our worflow to:
- Look for new data push by the Data Engineer of the WagonCab team in our database (the data eng will always push new data in our data source training table)
- Evaluate the performance of our current model in _Production_ (remember the mlflow stage ?) on the new data
- Train the latest model in _Production_ with the new data an see how the performance improves
- Communicate to the team the performance of the past and new models on the new data in order to decide whether to put the newly trained model in _Production_

Luckily for us, all the features are already backed in our existing `taxifare` package, so we only have to do the wiring and make sure that everything works correctly !

**💻 Complete the `taxifare.flow.main` and all the functions in the `taxifare.flow.flow` module (look for `# YOUR CODE HERE`)**

**✅ Try to `make run_flow`**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

  You do not need to write all the code right away before you test it: just put fake values in the return of the functions that you have not finished yet and observe what happens when you `make run_flow`.
</details>

### Leverage the Prefect suite

Now you have a functional workflow, sure you want to get the Prefect server + interface to play with.

1. Create an account on [Prefect Cloud](https://cloud.prefect.io/) and get an API key
1. Store your API key in a secret place 🙊
1. Launch a Prefect server (cf lecture)
1. Switch the `PREFECT_BACKEND_SERVER` to `production`

**💻 Try to `make run_flow`**

**✅ Check your workflow has been pushed to your Prefect dashboard**

Feel free to play with the UI to get familiar with.

🏁 Congrats! You plugged the `taxifare` to a full workflow lifecycle

</details>

## 3️⃣ Retrain on fresh data

How to exploit our workflow in order to automate periodical retraining on fresh data?

<details>
  <summary markdown='span'><strong>❓ Instructions (expand me)</strong></summary>

The `taxifare.flow` package is now ready for production.Now we want to make it run on several iterations of new incomings data.

The data engineer of the WagonCab team provide you with a few commands of their own crafting allowing you to inject new data iteratively in your data source, either on your local machine or in **Big Query**.

### Retrieve new data

❓ **How do you know which data is new in your data source ?**

The idea is to store in mlflow along with the training parameters the index of the last data row the model has seen during the latest training.

Luckily the tech team already though of this and the `first_row` and `row_count` parameters are already stored in mlflow on each training.

They even went as far as to provide you with a **mlflow** database schema in order to allow you to retrieve the data you are looking for.

<a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/mlflow-tables.png"><img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/mlflow-tables.png" width="150" alt="mlflow tables"></a>

And because they are very kind they also hand you a small piece of paper where the secret access codes for a read only account to the database are written in cypher:

```yaml
MLFLOW_DB_USER=taxifare_readonly
MLFLOW_DB_PASSWORD=m4e7dbNPDPg8tNR2Br36NgUGd3
MLFLOW_DB_HOSTNAME=wagon-mlflo-1768.postgresql.a.osc-fr1.scalingo-dbs.com
MLFLOW_DB_PORT=37750
MLFLOW_DB_NAME=wagon_mlflo_1768
```

**📝 Fill the `MLFLOW_DB_USER`, `MLFLOW_DB_PASSWORD`, `MLFLOW_DB_HOSTNAME`, `MLFLOW_DB_PORT` and `MLFLOW_DB_NAME` variables in the `.env` project configuration**

Once the codes are in your `.env`, find an appropriate way to destroy the small piece of paper 💣 🧨 💥 🔥

**🧪 Run the tests with `make test_mlflow_db_config`**

❓ **How do retrieve the rank of the next first row to be trained from?**

Use the `first_row` and `row_count` parameters in the mlflow database in order to process the index of the latest trained row.

👉 You should query the database from your code in order to retrieve these values.

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

  You can have a look at the structure of the database using **DBeaver**. Remember that `make show_env` will allow you to retrieve easily the parameters for the read only account to connect to the database. The database used by mlflow is a **Postgres** database (you need to specify the type of connection to create when using _DBeaver_).

</details>

**💻 Complete the `get_next_first_row` function in `taxifare.ml_logic.registry_db` module**

**✅ Try your function in ipython**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

In order to query the mlflow database from your code, you need a package able to connect to a _Postgres_ database. Let's use the _psycopg_ package that we have installed earlier.

Here is how you can query the database:

``` bash
import psycopg2
import psycopg2.extras

tracking_db_uri = os.environ.get("MLFLOW_TRACKING_DB")

conn = psycopg2.connect(tracking_db_uri)

cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

mlflow_query = """
SELECT * FROM experiments;
"""

cur.execute(mlflow_query)

results = cur.fetchall()
```

</details>

**💻 Update the `taxifare.flow.flow.py` file to use your brand new function to get the next first row**

```python
# flow.py
def get_next_training_params(experiment):
    #[...]
    # train on the whole dataset
        # this function will take meaning in the step 3 of the challenge
        # next_row = 0
        next_row = get_next_first_row(experiment)
```

**✅ Try to `make run_flow` and check both Mlflow UI and Prefect UI**

**🧪 Run the tests with `make test_get_next_first_row`**

### Simulate the passing of time

Let's play with the data engineer commands and see how the performance of our model behaves when we inject new data into the data source.

❓ **How do you inject new data in the data source ?**

The data engineer provided two sets of commands...

If you configured your `.env` so that your code sources the data from your local disk:
- `make reset_data_sources` will remove temporary data from your `data` directory
- `make show_data_sources` will show the data available for injection in your data source
- `make get_new_month` will inject one month worth of new data in your data source

If your code sources the data from Big Query:
- `make reset_bq_tables` will reset the Big Query dataset specified in your `.env`
- `make show_bq_tables` will show the state of your Big Query dataset tables
- `make push_month_to_bq` will inject one month worth of new data in your Big Query dataset table

Now your goal will be to alternate for example `make get_new_month` and `make run_flow` to inject new data and run a whole workflow lifecycle.

**💻 Run the `make get_new_month` and `make run_flow` commands until there is no more data to process**

**✅ Have a look at the evolution of the performance in the Mlflow UI**

🏁 Congrats! Your workflow lifecycle is ready to be shipped in production 🔥

</details>


