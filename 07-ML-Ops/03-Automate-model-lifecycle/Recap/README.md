
[//]: # ( challenge tech stack: mlflow prefect no-livecode )

[//]: # ( challenge instructions )

## ❓ TL;DR MLflow instructions

<details>
  <summary markdown='span'><strong>💻 Train a model from scratch on the 500k dataset</strong></summary>

  <details>
    <summary markdown='span'><strong>🎬 Setup the parameters</strong></summary>

    ``` bash
    cp .env.sample .env
    direnv allow
    direnv reload
    ```

  </details>

  <details>
    <summary markdown='span'><strong>🏋️‍♂️ Train the model</strong></summary>

    ``` bash
    make run_preprocess
    make run_train
    make run_evaluate
    ```
  </details>

  <details>
    <summary markdown='span'><strong>🏁 Put the model in production</strong></summary>

    In **MLflow** set the model _stage_ as _Production_
  </details>

</details>

<details>
  <summary markdown='span'><strong>💻 Handle the January dataset</strong></summary>

  <details>
    <summary markdown='span'><strong>🎬 Inject the dataset</strong></summary>

    ``` bash
    python get_new_data.py jan
    ```

  </details>

  <details>
    <summary markdown='span'><strong>👀 Observe the evolution of the performance</strong></summary>

    The performance of the model in production on the new data seems to be stable.

    👉 No need to train a new model

  </details>

</details>

<details>
  <summary markdown='span'><strong>💻 Handle other monthly datasets</strong></summary>

  <details>
    <summary markdown='span'><strong>🎬 Inject the monthly dataset</strong></summary>

    ``` bash
    python get_new_data.py jan
    ```

  </details>

  <details>
    <summary markdown='span'><strong>👀 Observe the evolution of the performance</strong></summary>

    👉 Define with the business a performance threshold on which to act, for example a variation of the performance of $0.3

    🤔 If the performance degrades significantly, train a new model

    🤔 If the performance of the new model is good enough, put it in production

  </details>

</details>

## ❓ TL;DR Prefect instructions

<details>
  <summary markdown='span'><strong>💻 Workflow setup and local visualize</strong></summary>

  <details>
    <summary markdown='span'><strong>🔑 Authenticate to Prefect</strong></summary>

    ``` bash
    prefect auth login -k YOUR_KEY
    ```

  </details>

  <details>
    <summary markdown='span'><strong>🎬 Start a Prefect agent</strong></summary>

    ``` bash
    prefect agent local start
    ```

  </details>

  <details>
    <summary markdown='span'><strong>👀 Visualize the workflow locally</strong></summary>

    ``` bash
    make run_workflow
    ```

  </details>

</details>

<details>
  <summary markdown='span'><strong>💻 Workflow quick run</strong></summary>

  <details>
    <summary markdown='span'><strong>📝 Register the workflow in Prefect Cloud</strong></summary>

    Set `PREFECT_BACKEND=production` in the `.env` and `direnv reload`.

    In the `taxifare.flow.main` module, comment out the `LocalDaskExecutor` line.

    ``` bash
    make run_workflow
    ```

  </details>

  <details>
    <summary markdown='span'><strong>🚕 Quick run the workflow</strong></summary>

    Run the workflow in the Prefect UI using _Quick Run_.

  </details>

  <details>
    <summary markdown='span'><strong>👀 Observe the performance in the notification app</strong></summary>

    Check the performance in [https://wagon-chat.herokuapp.com/<user.github_nickname>].

  </details>

</details>

<details>
  <summary markdown='span'><strong>💻 Run the automated workflow</strong></summary>

  <details>
    <summary markdown='span'><strong>📆 Schedule the workflow</strong></summary>

    Create a schedule in the Prefect UI.

  </details>

  <details>
    <summary markdown='span'><strong>♻️ For each month</strong></summary>

    💉 Inject new data

    👀 Observe the performance in the notification app

    🤔 Put the newly trained model in production if appropriate

  </details>

</details>

<details>
  <summary markdown='span'><strong>💻 Optimize the workflow</strong></summary>

  <details>
    <summary markdown='span'><strong>📝 Register a parallel version of the workflow</strong></summary>

    In the `taxifare.flow.main` module, uncomment the `LocalDaskExecutor` line.

    ``` bash
    make run_workflow
    ```

  </details>

  <details>
    <summary markdown='span'><strong>👀 Observe the workflow evolution</strong></summary>

    In the Prefect UI, the workflow tasks execute in parallel whenever possible.

  </details>

</details>

## MLflow

Let's track the evolution of the performance of our model accross time using **MLflow**.

### Setup

Let's create a `.env` file:

``` bash
cp .env.sample .env
```

And setup the local data path in the `.env`:

``` bash
LOCAL_DATA_PATH=~/.lewagon/mlops/data
LOCAL_REGISTRY_PATH=~/.lewagon/mlops/training_outputs
```

Then `direnv allow .` and `direnv reload` and retrieve the latest version of the data using either:
- `make reset_sources_all` in order to reset datasets of all sizes in local disk + Big Query
- `make reset_sources_env` in order to reset datasets of size `DATASET_SIZE` / `VALIDATION_DATASET_SIZE` in local disk + Big Query

Create an account on [Prefect Cloud](https://www.prefect.io/) if you do not have one.

### Past data

Let's train the model with an initial `500k` dataset with:

``` bash
DATASET_SIZE=500k
VALIDATION_DATASET_SIZE=500k
CHUNK_SIZE=1000000

DATA_SOURCE=local
MODEL_TARGET=mlflow
```

👉 We boosted the chunk size and use local CSV in order to improve the speed of the trainings

Make sure to update the _MLflow_ and _GCP_ (for _Big Query_) parameters:
- `MLFLOW_EXPERIMENT`
- `MLFLOW_MODEL_NAME`
- `PROJECT`
- `DATASET`

Update and reload your `.env`, then train the model and observe the raw performance in `mlflow`:
- `make run_preprocess`
- `make run_train`

### New data

Now that the initial model is trained and stored in **MLflow**, let's inject new data and see how the model behaves.

Update and reload your `.env` to play with the new data source:

``` bash
DATASET_SIZE=new
VALIDATION_DATASET_SIZE=new
```

For January, February and March:
- Inject new data with `python get_new_data.py jan`
- Preprocess the data with `make run_preprocess`
- Observe how the model in production performes on the new data with `make run_evaluate`
- If the model performance degrade more than $.1, train a new model from the model in production with `make run_train`
- Observe the performance of the new model
- If the performance of the new model is good enough, annotate the new model to be in production in **mlflow**

👉 Performance should be stable in January and start to evolve from February

## Prefect

Now that we understand how to track the performance of our model, let's automate the model lifecycle.

Authenticate to Prefect Cloud with `prefect auth login -k YOUR_KEY`.

Start a local agent so that the outcome of the workflow runs on your machine are persisted in **Prefect**.

### Reset your data source

Let's go through our datasets all over again, but this time using **Prefect** in order to automate everything.

We want to start over from the latest model having been trained from scratch on the `500k` dataset.

Go to **MLflow** and mark the latest model trained from scratch on the `500k` dataset as in `Production`.

### Sequential workflow

Update and reload your `.env` with parameters for Prefect Cloud:

``` bash
PREFECT_BACKEND=production
PREFECT_FLOW_NAME=taxifare_lifecycle_<user.github_nickname>
```

👉 Make sur your project exists in Prefect Cloud (the default is `taxifare_project`)

Register your workflow:

``` bash
make run_workflow
```

Connect to Prefect Cloud:
- 👀 Navigation: verify that your workflow has been uploaded
- 👀 Agents: verify that your local agent is running

### Go through months

Let's inject the _January_ dataset with `python get_new_data.py jan`.

Then run the workflow once through the Prefect Cloud UI:
- 👀 Quick run

👉 Now that everything is connected, we can schedule the workflow to run automatically

Configure the `channel` in `taxifare.flow.flow` module.

Schedule the workflow in the Prefect Cloud UI:
- 👀 Schedules

Have a look at the notification board: https://wagon-chat.herokuapp.com/

### Parallel workflow

The sequential workflow is pretty slow, let's see how we can run it faster.

In the `taxifare.flow.flow` module, uncomment the `LocalDaskExecutor` line.

Register the new workflow using `make run_workflow`.

In the Prefect Cloud UI:
- 👀 Task run: have a look at the logs
