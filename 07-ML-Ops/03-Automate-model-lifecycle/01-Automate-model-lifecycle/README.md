
[//]: # ( presentation of the unit )

**🥁 Discover model lifecycle automation and orchestration 🎻**

In the previous unit, you implemented a full model lifecycle in the cloud:
1. Sourcing data from a Data Warehouse
1. Launching a training on a Virtual Machine, along with evaluating the model performance and making predictions
1. Storing the trained model in a bucket

>The _WagonCab_ is really happy with your work and assign you on a new mission: **Ensure the validity of the trained model through time.**

As you can imagine, the fare amount of a taxi ride is meant to evolve through time and the model could be accurate right now but obsolete in the very future.

---

🤯 After a quick brainstorm with your team, you come with a plan:
1. Implement a process to monitor the performance of the `Production` model through time
1. Implement a automated workflow which:
    - Fetch the fresh data
    - Preprocess the fresh data
    - Evaluate the performance of the `Production` model
    - Train a `Staging` model on the fresh data, _in parallel of the above task_
    - Compare `Production` vs `Staging` performance
    - Notify a human who decides to deploy the `Staging` model to `Production` _or not_
1. Deploy this workflow and wait for fresh data to come

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/wagoncab_workflow.png" alt="wagoncab_workflow" width=500>


# 1️⃣ SETUP

Get your project ready for this new mission 🚀

<details>
  <summary markdown='span'><strong>❓ Instructions (expand me)</strong></summary>

## Install requirements

**💻 Install the version `0.0.7` of the `taxifare` package with `make reinstall_package`**

Notice we've added 3 new packages: `mlflow`, `prefect` and  `psycopg2`

In addition, you need to install 2 binaries [Graphviz](https://graphviz.org/) and [xdg-utils](https://www.freedesktop.org/wiki/Software/xdg-utils/) to make Prefect work smoothly:

<details>
  <summary markdown='span'>⚙️ Mac OSX</summary>

```bash
brew install graphviz
```

</details>

<details>
  <summary markdown='span'>⚙️ Ubuntu</summary>

```bash
sudo apt install graphviz xdg-utils
```

</details>

**✅ Check your `taxifare` package version**

```bash
pip list | grep taxifare
# taxifare                  0.0.7
```

**💻 Do not forget to handle your `.env` file**

_copy_ the `.env.sample`, _fill_ the `.env`, _allow_ `direnv`


## Reset all data sources

Start your mission refreshing all your data sources:
- CSVs datasets
- BigQuery tables

We provide you with a command which download all the CSVs locally and generate all the tables in your data warehouse.

**💻 Run `make reset_sources_all`** (~300Mo downloads)

**✅ Check both your `~/.lewagon/mlops/data` directory and your `taxifare_dataset` BigQuery dataset  have been filled**

**📝 Edit the `.env` file to work with the `train_10k` and `val_10k` datasets, and `CHUNK_SIZE=10000`** (let's start light)

🏁 You are up and ready!
</details>

<br>


# 2️⃣ PERFORMANCE MONITORING WITH ML FLOW

- Use **mlflow** to store the trained models and the result of our experiments in the cloud
- Monitor the evolution of the performance of our models experiment after experiment

<details>
  <summary markdown='span'><strong>❓ Instructions (expand me)</strong></summary>

[//]: # ( challenge tech stack: mlflow )

## Configure your project for mlflow

### Mlflow server

> The **WagonCab** tech team put in production a **mlflow** server located at [https://mlflow.lewagon.ai](https://mlflow.lewagon.ai) you will use in to track your experiments and store your trained models.

### Environment variables

👀 Look at your `.env` file and discover 3 new variables:
- `MODEL_TARGET` which defines how the `taxifare` package should save the _outputs of the training_ (i.e. the trained _model_, the training _parameters_ and _metrics_) once the training is over. `MODEL_TARGET` can take 2 values: `local` or `mlflow`
- `MLFLOW_EXPERIMENT` which is the name of the experiment
- `MLFLOW_MODEL_NAME` which is the name of your model

**📝 Edit your `.env` project configuration file:**

- `MODEL_TARGET` with the corresponding value
- `MLFLOW_EXPERIMENT` should contain `taxifare_experiment_<user.github_nickname>`
- `MLFLOW_MODEL_NAME` should contain `taxifare_<user.github_nickname>`

**🧪 Run the tests with `make test_mlflow_config`**

Now your mlflow config is set up, you need to update your package so the trained **model**, its **params** and its **performance** are pushed to mlflow anytime you are running an new experiment, i.e. a new training.

## Push your train results to MLFLOW

### Step 1: Push the `params`

**❓ Which module of your `taxifare` package is responsible for saving the training outputs?**

<details>
  <summary markdown='span'>Answer</summary>

It is the role of the `taxifare.ml_logic.registry` module to save the trained model, its parameters, and its performance thanks to the `save_model()` function.

This function is called anytime the model is trained or evaluated.
</details>

**❓ What are the training parameters?**

<details>
  <summary markdown='span'>Answer</summary>

Have a look at the `taxifare.interface.main` module, the `train()` function send a `dict` of parameters to the `save_model()` function:

```python
# main.py
def train():
    # [...]
    params = dict(
        # model parameters
        learning_rate=learning_rate,
        batch_size=batch_size,
        model_version=get_model_version(), # 💡 New method added for you, to log the model version from which to partial-train from
        # package behavior
        context="train",
        chunk_size=CHUNK_SIZE,
        # data
        training_set_size=DATASET_SIZE,
        val_set_size=VALIDATION_DATASET_SIZE,
        row_count=row_count,
        dataset_timestamp=get_dataset_timestamp(), # 💡 New method added for you, to log the "date" of the train_dataset
    )

    # save model
    save_model(model=model, params=params, metrics=dict(mae=val_mae))
```

</details>

**💻 Complete the first step of the `save_model` function in the `taxifare.ml_logic.registry` module**

```python
# registry.py
def save_model():
    # [...]
    # retrieve mlflow env params
    # YOUR CODE HERE

    # configure mlflow
    # YOUR CODE HERE

    if os.environ.get("MODEL_TARGET") == "mlflow":
        #[...]
        with mlflow.start_run():
            # STEP 1: push parameters to mlflow
            # YOUR CODE HERE

            # STEP 2: next question, keep empty
            # STEP 3: next question, keep empty
```



**🧪 Try to run the training using `make run_train`**

**✅ Check on the [mlflow interface](https://mlflow.lewagon.ai) if your parameters have been pushed**

<details>
  <summary markdown='span'>💡 Hint </summary>
  Have a look at the [mlflow python API documentation](https://mlflow.org/docs/latest/python_api/mlflow.html).

  Do not forget to set the tracking server with `mlflow.set_tracking_uri` and to provide an experiment name with `mlflow.set_experiment`.

  You should get something like this:

  <img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/mlflow_push_params.png" alt="mlflow_experiment" width=500 />
</details>

### Step 2: Push the `metrics`

Let's now push the metric (MAE) to mlflow.

**💻 Complete the second step of the `save_model` function in the `taxifare.ml_logic.registry` module**
- Try to run the training again using `make run_train`
- Check your metric has been pushed to mlflow

<details>
  <summary markdown='span'> 💡 Hint </summary>
  You should get something like this:

  <img src='https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/mlflow_push_metric.png' alt='mlflow_push_metric' width=500 />
</details>


### Step 3: Push the `model`

Now for the better part: mlflow allows us to store the trained model so that we can easily refer to it when we want to make a prediction. This will allow you colleagues to use smoothly the model you have trained !

**💻 Complete the third step of the `save_model` function in the `taxifare.ml_logic.registry` module**
- Have a look at the [mlflow python API for Keras](https://mlflow.org/docs/latest/python_api/mlflow.keras.html) and find a function allowing you to upload your trained model.
- Try to run a training using `make run_train`
- Check your model has been pushed to mlflow

<details>
  <summary markdown='span'> 💡 Hint </summary>
  You should get something like this:

  <img src='https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/mlflow_push_model.png' alt='mlflow_push_model' width=500 />

</details>


## Monitor model performance through `DATASET_SIZE`

You have a nice way to save your training outputs! Now is the time to train your model and monitor its performance. Let's start a set of experiments increasing the `DATASET_SIZE` and observe the consequence on the validation MAE.

**💻 Launch some training runs increasing the dataset size from 10k to 500k**
- Take the same size for the training set and the validation set
- Use 1 or 2 chunks for dataset size <= 100k
- Use chunks of 100k for dataset size > 100k
- Use your local data source to speed-up the process!


**👀 Inspect your performance evolution through `DATASET_SIZE` on mlflow**
<details>
  <summary markdown='span'> 💡 Hints: </summary>

  You should get something like this:

  <img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/mlflow_perf_training_set_size.png" alt="mlflow_perf_training_set_size" width=500 />

</details>


**💻 Put your _best_ model in `Production` stage in the mlflow UI**

## Make a prediction from you model saved in mlflow

What's the point storing my model in mlflow you'll say ? Well for starters mlflow allows you to handle very easily the lifecycle stage (_None_, _Staging_ or _Production_) of the model in order to synchronize the information accross the team. And more importantly, it allows any application to load a trained model in a given stage in order to make a prediction.

**💻 Complete the `load_model` function in the `taxifare.ml_logic.registry` module, then run a prediction using `make run_pred`**

<details>
  <summary markdown='span'> 💡 Hint </summary>

  Have a look at the [mlflow python API for Keras](https://mlflow.org/docs/latest/python_api/mlflow.keras.html) and find a function allowing you to retrieve your trained model.
</details>

🏁 Congrats! Your `taxifare` package is now persisting every aspect of your experiments in **mlflow** and you have _production-ready_ model.

</details>

<br>

# 3️⃣ RETRAIN ON FRESH DATA

Exploit our workflow in order to retrain on fresh data 🆕

<details>
  <summary markdown='span'><strong>❓ Instructions (expand me)</strong></summary>

So far you are able to track the `taxifare` model performance and choose which model version you want to set in `Production` for prediction purpose. That's good but your mission is not over yet. You need to monitor model performance through **time** when **new data** is available so you can ensure the predictions remain **accurate**.

Here are the next steps you decide to work on:
- Simulate new data incoming
- Evaluate the `Production` model on new data
- Re-train on new data **only**

## Simulate the passing of time

> The _WagonCab_ Data Engineering Team gave you a nice input: you can get 100k new records per month, already split chronologically between two 80k "train_new" and 20k "val_new" raw datasets. As the previous trainings showed you that this amount of data is enough to get a very good model performance, let's trigger the workflow **every month**. But wait, you ain't time to wait for it! You need to test your workflow right now! The good news is the Data Engineering Team has just finished to collect and prepare the data from January and February:

**👀 Inspect the `get_new_data.py` file that was given to you by the engineering team**
- It is located at the root directory because it's not part of your taxifare package.

**💻 Try to download data for January**
- 💡 You can run `python get_new_data.py -h` to get some help.
- ✅ Check you have the new CSVs locally and the new table on your data warehouse**

## Monitor the performance metric on new data

Now you fetched the new data, you need to check how the `Production` model performance is evolving.

**📝 Edit the `.env` file so you will be able to work with the new data:**
```bash
DATASET_SIZE=new
VALIDATION_DATASET_SIZE=new
CHUNK_SIZE=100000 # In this challenge, we won't need multiple chunks as a "100k" new dataset is small enough
```

**💻 Evaluate the model performance on January data**

<details>
  <summary markdown='span'>Hints</summary>

You can use the `taxifare.interface.main` (ie. `make run_...` ) to:
1. Preprocess the new training set
2. Preprocess the new validation set
3. Evaluate the `Production` model performance on new data (don't train it!)

Then you can check the MAE on mlflow.
</details>

**💻 Retrieve one more month of data (February), and evaluate again it's performance**

You should start noticing that your Production model performance decreases with time!

The MAE increased of about 15¢ is significative (we should cross-validate our model to be sure, but we don't have time for that in this challenge). It means that external conditions changed so that the `Production` model is not fit for purpose anymore. You need to re-train it with the new data to decide if whether or not you need to deploy a new model.

## Update the `Production` stage model weights

**💻 Re-train the `Production` model on new data with `make run_train`**

**👀 Compare the `Production` model evaluation with the new model MAE on mlflow**

**❓ Would do deploy the new model version to `Production`?**
<details>
  <summary markdown='span'>Anwser</summary>

Yes! The validation MAE of your re-trained (incrementally) production model is better than that of your original production model. And this result has been evaluated on the very same validation set of 40,000 rows - a significant size that can be considered representative of the current february period. You should therefore deploy this new one to production!

</details>


**💻 Loop over the workflow one last time with the new data from March**

<details>
  <summary markdown='span'>ℹ️ Info</summary>

- You can start over your "january --> june" journey at any moment with the `make delete_new_source` command
- You can very well call `get_new_month('mar')` without having called it with `jan` or `feb` before.
- These methods simply erase and replace what's inside `train_new.csv` and `val_new.csv` (and warehouse table equivalents)

</details>

👉 You can even play with the mlflow interface to plot the performance metrics through time!
👉 As months pass by, are you as happy with your new model performances compared with january ?


<details>
  <summary markdown='span'>👍 ML Eng Pro Tips </summary>

Why does my production performance deteriorates slightly even after new incremental training?

1. As an ML Engineer who knows the best practices, you should **retrain** again the model on the **whole 100k new data** so you fully exploit the info.
2. As an ML Engineer who understands deep-learning, you should always try to **finetune** a model by playing with `batch_size`,  `learning_rate` and `patience` available to you at `taxifare.interface.main.train`. Indeed, incremental training (i.e retraining an existing model on new data while keeping its existing weights) implies a trade-off between long and short term memory models. Do you want to put more weights on NEW data, or on PREVIOUS ones?

These two points are outside of this module's scope, but keep them in mind for your first interviews!

</details>

🏁 Congrats! Your workflow lifecycle is ready to be shipped in production 🔥

</details>

<br>

# 4️⃣ AUTOMATE MODEL LIFECYCLE WITH PREFECT

- Automate your workflow with **Prefect**
- Keep a human in the loop 🤓

<details>
  <summary markdown='span'><strong>❓ Instructions (expand me)</strong></summary>

> Good news! The WagonCab tech team tasked an intern to provide you with the **Prefect** boilerplate 🤩

## Workflow package structure

Here are the new files added by the intern:

``` bash
.
└── taxifare
    ├── flow
    │   ├── flow.py     # ♻️ workflow lifecycle code
    │   └── main.py     # 🚀 workflow launcher
    ├── data_sources
    ├── interface
    └── ml_logic
```

### `taxifare.flow.flow`
The trainee provided you with a full **Prefect** workflow boilerplate that they think will best allow you to plug the `taxifare` and build a complete automation for its lifecycle.

### `taxifare.flow.main`
The intern provided an entry point allowing you to trigger **ONE** run of the model lifecycle thanks to the `make run_workflow` command.

## Configure your project for Prefect

❓ **What parameters do you need to interact with Prefect ?**

**📝 Edit your `.env` project configuration file:**
- `PREFECT_FLOW_NAME` should follow `taxifare_lifecycle_<user.github_nickname>` convention
- `PREFECT_LOG_LEVEL` variable to `WARNING`(more info [here](https://docs.prefect.io/core/concepts/logging.html)).

**🧪 Run the tests with `make test_prefect_config`**

## Complete the workflow

❓ **How do you complete the workflow ?**

Our goal is to be able to run the workflow in an automated way.

We want our worflow to:
- Preprocess the new data
- Evaluate the performance of our current model in _Production_ (remember the mlflow stage ?) on the new data
- Train the latest model in _Production_ with the new data an see how the performance changes

**💻 Complete the tasks and the `build_flow()` function within `taxifare.flow.flow` module**

**✅ Try to `make run_workflow`**

**👀 Inspect the mlflow UI to see your workflow logs**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

  You do not need to write all the code right away before you test it: just put fake values in the return of the functions that you have not finished yet and observe what happens when you `make run_workflow`.
</details>

## Stay tuned

> Congrats! The _WagonCab_ team is impressed with your automated workflow but wait, wait! The Product Manager notes your workflow is missing **one last step**, don't you think? Exactly, you would like to be notified as soon as a workflow finishes. You know that  Prefect comes with a [couple of ways](https://docs-v1.prefect.io/api/latest/tasks/notifications.html) to do so. But the Product Manager would like you to use their own internal chat so the whole data team will be able to stay tuned.

**💻 Implement the `notify` task**

```python
# flow.py
import requests

@task
def notify(eval_mae, train_mae):
    base_url = 'https://wagon-chat.herokuapp.com'
    channel = '<user.github_nickname>' # change to your batch number when ready
    url = f"{base_url}/{channel}/messages"
    author = '<user.github_nickname>'
    content = "Evaluation MAE: {} - New training MAE: {}".format(
        round(eval_mae, 2), round(train_mae, 2))
    data = dict(author=author, content=content)
    response = requests.post(url, data=data)
    response.raise_for_status()
```

**💻 Update the `build_flow()` function then `make run_flow` again**

**✅ Check your notification on [https://wagon-chat.herokuapp.com/<user.github_nickname>](https://wagon-chat.herokuapp.com/<user.github_nickname>)**

<details>
  <summary markdown='span'>ℹ️ Wagon Chat API</summary>

[LeWagon Chat API](http://github.com/lewagon/wagon-chat-api) plays a role in the [Web Development Bootcamp](https://www.lewagon.com/web-development-course/full-time) while students are learning to communicate with API and the fundamentals of [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript).
</details>

## Leverage the Prefect suite

Great, you now you have a functional prefect workflow that you can run locally when `PREFECT_BACKEND_SERVER` is set to `development`.

However, Prefect also comes with an online server + UI to play with!

1. Create an account on [Prefect Cloud](https://cloud.prefect.io/) and get an API key
2. Store your API key in a secret place 🙊
3. Auth to Prefect using your API key (cf lecture)
4. Launch a Prefect Agent (cf lecture)
5. Switch the `PREFECT_BACKEND_SERVER` to `production`

☝️ In production mode, `make run_workflow` do not execute any computation at all! It just sends a "snapshot" of your taxifare package to Prefect Cloud web server (but does not execute it). Therefore, you will need to re-run this anytime you change your code or your `.env` locally.

**💻 Try to `make run_workflow` and check that your workflow has been pushed to your Prefect dashboard**

Now, because you have also launched a Prefect Agent that connects your local machine and the Prefect Cloud web server, you will be able to click on "Quick Run" on the Prefect Cloud UI to trigger the workflow locally on your machine without resorting to your terminal anymore. (Think, for instance, that your local machine is instead a powerfull remote server full of GPUs... You do not need to SSH-connect to it every time you want to launch a training !)

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/prefect_quick_run.png" width=500>

👉 **Actually execute your workflow from the Prefect UI**
- 🔎 Find and run your workflow in the Prefect UI
- Check the performance of your model on MLFLOW

👏👏👏👏 Congrats for plugging the `taxifare` to a fully automated workflow lifecycle

**🏁 Have fun to finish with!**
1. Start back with data from January 2015
2. Execute your workflow with Prefect
3. Simulate the passing of time with the `get_new_data()` function
4. Follow the chat to check for notifications
5. Use the **Compare** feature of the MLflow UI to draw performance metric data visualization
6. Set the last best model to `Production` anytime with MLflow
7. Move forwards one month and repeat ! You can even try to schedule your workflow to be ran every 5 minutes instead of manually using "Quick Run" 📆

</details>

<br>

# 5️⃣ OPTIONALS

<details>
  <summary markdown='span'><strong>❓ Instructions (expand me)</strong></summary>

## OPTIONAL 1: Parallelization

1. Use the [`prefect.executors.LocalDaskExecutor`](https://docs-v1.prefect.io/core/tutorial/06-parallel-execution.html#scaling-out) in `flow.main.py` to parallelize the tasks
1. Launch the new workflow in `development` mode to test it then go to `production` and visualize the effect on the execution time
1. Identify the existing task which can be split and parallelized
1. Create a `flow.parallelized_flow.py` based on the previous workflow and adapt it so the formerly identified task is split
1. Publish and run the new workflow and check the new execution time

## OPTIONAL 2: Model Finetuning

1. Before deciding which model version to put in production, try a couple of hyperparameters during the training phase, by testing (grid-searching?) wisely various `batch_size`,  `learning_rate` and `patience`.
1. In addition, after finetuning and deciding on a model, try to retrain using the whole new dataset of each month, and not just the "train_new".

</details>
