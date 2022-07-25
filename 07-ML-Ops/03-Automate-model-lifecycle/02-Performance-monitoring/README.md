
[//]: # ( presentation of the unit )

**🥁 Discover model lifecycle automation and orchestration 🎻**

In this unit, you will learn how to orchestrate and automate the lifecycle of your model.

You will see how to formalise the structure of the model lifecycle broken down into a set of tasks and how to organise these tasks together.

You will create an automated workflow for the **TaxiFare** 🚕 model that periodically runs the whole model lifecycle on remote machines in order to consume the new data that is regularly injected into your data source.

You will store monitoring data 🔎 to ensure that your model continues to perform correctly while you are away 🏝

[//]: # ( unit tech stack: )

[//]: # ( presentation of the challenges of the unit )

## Unit challenges

**1️⃣ Performance monitoring**
- Use **mlflow** to store the trained models and the result of our experiments in the cloud
- We will monitor the evolution of the performance of our models on new data over time

**2️⃣ Your first DAG**
- Let's discover how to split and structure the model lifecycle into a **Direct Acyclic Graph** of tasks
- How to schedule a DAG ?

**3️⃣ Retrain on fresh data**
- How to exploit our workflow in order to automate periodical retraining on fresh data?

**4️⃣ Simulate Data Distribution Shifts**
- How to adapt our workflow in order to handle the variations of data distribution over time?

**5️⃣ Trigger work on a Compute Engine**
- How can we automate the training of a model by trigerring a job on a **Compute Engine**

**6️⃣ Automated lifecycle**
- We will build a workflow to retrain periodically the model with fresh data and monitor the performance of the new model
- But always keep a human 👀 in the loop

**▶️ Recap - Data versioning**
- Discover how to leverage **Git LFS** and **DVC** in order to version your datasets

[//]: # ( challenge tech stack: mlflow )

**💻 Install the package of the current challenge with `make reinstall_package`**

**💻 Do not forget to handle your `.env` file (_copy_ the `.env.sample`, _fill_ the `.env`, _allow_ `direnv`)**

[//]: # ( challenge instructions )

## Configure your project for mlflow

First let's install some additional package required in order to connect to the mlflow database. It will allow the tests to run correctly.

``` bash
pip install psycopg2-binary
```

The **WagonCab** tech team put in production a **mlflow** server located at https://mlflow.lewagon.ai. This will be useful in order to track your experiments and store your trained models.

We added a new variable to the `.env` project configuration file so that the `taxifare-model` package is able to push to **mlflow** the _trained model_ along with the training _parameters_ and _metrics_ once the training is over.

❓ **What parameters do you need to interact with mlflow ?**

Edit your `.env` project configuration file and set the `MODEL_TARGET` parameter to `mlflow`. Now your code will try to push the trained model to mlflow once the training is complete.

You also need to define unique experiment and model names since the server is shared between all the members of the company.

Follow these patterns in order to be able to find your experiment easilly:
- `MLFLOW_EXPERIMENT` should contain `taxifare_experiment_<user.github_nickname>`
- `MLFLOW_MODEL_NAME` should contain `taxifare_<user.github_nickname>`

You will also need to set in the project configuration the tracking URI of the mlflow server: `https://mlflow.lewagon.ai`.

**📝 Fill the `MODEL_TARGET`, `MLFLOW_EXPERIMENT`, `MLFLOW_MODEL_NAME`, and `MLFLOW_TRACKING_URI` variables in the `.env` project configuration**

**🧪 Run the tests with `make dev_test`**

👉 `test_mlflow_parameters` should be ✅

## Push your parameters

❓ **How do you push your training parameters to mlflow ?**

Let's update the code to push the experiment parameters to mlflow once the training it done.

Make sure to push either `learning_rate`, `batch_size` or `context` (the `if __name__ == '__main__': code` in the `taxifare_model.interface.main` module already does that)

**💻 Append the `save_model` function in the `taxifare_model.ml_logic.registry` module, then run a training**

**🧪 Run the tests with `make dev_test`**

👉 `test_mlflow_push_params` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

  Have a look at the [mlflow python API documentation](https://mlflow.org/docs/latest/python_api/mlflow.html).

  Do not forget to set the tracking server with `mlflow.set_tracking_uri` and to provide an experiment name with `mlflow.set_experiment`.
</details>

## Push your metrics

❓ **How do you push your training metrics to mlflow ?**

Let's now push the metrics to mlflow. The code should be almost the same as for the parameters of the experiment.

Make sure to push either `val_mae`, `mean_val` or `mae` (the code already does that)

**💻 Append the `save_model` function in the `taxifare_model.ml_logic.registry` module, then run a training**

**🧪 Run the tests with `make dev_test`**

👉 `test_mlflow_push_metrics` should be ✅

## Push your trained model

❓ **How do you push your trained model to mlflow ?**

Now for the better part: mlflow allows us to store the trained model so that we can easily refer to it when we want to make a prediction.

This will allow you colleagues to use smoothly the model you have trained !

**💻 Complete the `save_model` function in the `taxifare_model.ml_logic.registry` module, then run a training**

**💻 Put your model in Production in the mlflow UI**

**🧪 Run the tests with `make dev_test`**

👉 `test_mlflow_push_model` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  Have a look at the [mlflow python API for Keras](https://mlflow.org/docs/latest/python_api/mlflow.keras.html) and find a function allowing you to upload your trained model.
</details>

## Make a prediction from you model saved in mlflow

What use is it to store my model in mlflow you say ? Well for starters mlflow allows you to handle very easily the lifecycle stage (_None_, _Staging_ or _Production_) of the model in order to synchronize the information accross the team. And more importantly, it allows any application to load a trained model in a given stage in order to make a prediction.

❓ **How do you make a prediction from a trained model stored in mlflow ?**

**💻 Complete the `load_model` function in the `taxifare_model.ml_logic.registry` module, then run a training**

**🧪 Run the tests with `make dev_test`**

👉 `test_mlflow_pred_model` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  Have a look at the [mlflow python API for Keras](https://mlflow.org/docs/latest/python_api/mlflow.keras.html) and find a function allowing you to retrieve your trained model.
</details>

🏁 Congrats! Your `taxifare-model` package is now persisting every aspect of your experiments in **mlflow**
