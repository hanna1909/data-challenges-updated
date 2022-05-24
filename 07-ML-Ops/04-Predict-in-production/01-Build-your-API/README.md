[//]: # ( challenge tech stack: fastapi uvicorn )

[//]: # ( challenge instructions )

## Objective

Use **FastAPI** in order to create an API for your model.

Run that API on your machine.

## Context

Now that we have a performant model trained in the cloud, we will expose it to the world 🌍

We will create a **Prediction API** for our model, run it on our machine in order to make sure that everything works correctly. Then we will deploy it in the cloud so that everyone can play with our model!

In order to do so, we will:
- Challenge 1 : create a **Prediction API** using **FastAPI**
- Challenge 2 : create a **Docker image** containing the environment required in order to run the code of our API
- Challenge 3 : push this image to **Google Cloud Run** so that it is instantiated as a **Docker container** that will run our code and allow developers all over the world to use it

## Project setup

### API directory

We will start with a clean slate for these challenges. The project on which we will be working is similar to the codebase you worked with until now, but now you have a new directory: `/api`.

First, let's have a look at this new directory:

```bash
.
├── Makefile            # Good all task manager
├── requirements.txt    # All you need to pip install
├── setup.py            # The package installer
└── taxifare_api        # Package directory
    ├── __init__.py
    └── fast.py         # Where the API lays
```

**❓ What's inside that new directory?**

<details>
    <summary markdown='span'>Answer</summary>

🎁 As you can see, it contains a new **package** named **`taxifare_api`** you are going to implement!

</details>
<br>

Now, navigate into the `/api` directory, your terminal may pop you with some **errors or warnings**.

**❓ How would you solve these errors or warnings?**

<details>
    <summary markdown='span'>💡 Hints</summary>

A new package means a new virtual env...
</details>

### Running the API with FastAPI and a Uvicorn server

We provide you with with a FastAPI skeleton in the `fast.py` file.

**💻 Launch the API**

<details>
    <summary markdown='span'>💡 Hint</summary>

You probably need a `uvicorn` web server..., with a hot reloading...
</details>
<br>

**🐛 The server logs may throw some errors, try to fix them before moving forward.**

**💻 Once you find the right command and the API runs without crashing, feel free to fill in your `Makefile` with a `run_api` task.**

**❓ How do you consult your running API?**

<details>
    <summary markdown='span'>Answer</summary>

💡 Your API is available on a local port, `8000` probably 👉 [http://localhost:8000](http://localhost:8000).

</details>
<br>

**❓ Which endpoints are available?**

<details>
    <summary markdown='span'>Answer</summary>

There is only one endpoint _partially_ implemented at the moment, the root endpoint `/`.
</details>

## Build the API

An API is defined by its specifications. E.g. [GitHub repositories API](https://docs.github.com/en/rest/repos/repos). You will find below the API specifications you need to implement.

### Specifications

#### Root

- GET `/`
- Response
Status: 200
```json
{
    'greeting': 'Hello'
}
```

**💻 Implement the Root endpoint `/`**

**👀 Look at your browser 👉 [http://localhost:8000](http://localhost:8000)**

**🐛 Inspect the server logs and add some `breakpoint()` to debug**

Once and _only once_ your API responds as required:
**🧪 Test your implementation with `make test_root`**

**🚀 Commit and push your code!**

#### Prediction

- GET `/predict`
- Query parameters

| Name | Type |
|---|---|
| pickup_datetime | DateTime `2013-07-06 17:18:00` |
| pickup_longitude | float `-73.950655` |
| pickup_latitude | float `40.783282` |
| dropoff_longitude | float `-73.950655` |
| dropoff_latitude | float `40.783282` |
| passenger_count | int `2` |

- Response
Status 200
- Code sample
GET `http://localhost:8000/predict?pickup_datetime=2013-07-06 17:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2`
Example response:
```json
{
    'fare_amount': 5.93
}
```
**❓ How would you proceed to implement the `/predict` endpoint? 💬 Discuss with your buddy.**

<details>
    <summary markdown='span'>💡 Hints</summary>

Ask yourselves the following questions:
- How should we handle the query parameters?
- How can we re-use the `taxifare_model` package?
- How can we import the `taxifare_model` package?
- How should we build `X_pred`? What does it look like?
- How to render the correct response?
</details>

<details>
    <summary markdown='span'>🍔 Food for thought</summary>

1. Investigate the data types of the query parameters, you may need to convert them into the types the model requires
1. Of course you must re-use the `taxifare_model.interface.main.pred()` or the `taxifare_model.ml_logic.registry.load_model()` functions!
1. Did you know that you can install a requirement from a package stored in a GitHub repository? Use the last available solution.
1. In order to make a prediction with the trained model, you must provide a valid `X_pred` but the `key` is missing!
1. FastAPI can only render data type from the Python Standard Library, you may need to convert `y_pred` to match this requirement
</details>
<br>

**👀 Inspect your browser response 👉 ['http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2](http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2)**

**🐛 Inspect the server logs and add some `breakpoint()` to debug**

Once and _only once_ your API responds as required:
**🧪 Test your implementation with `make test_predict`**

**🚀 Commit and push your code!**

**👏 Congrats, you build your first ML API!**
