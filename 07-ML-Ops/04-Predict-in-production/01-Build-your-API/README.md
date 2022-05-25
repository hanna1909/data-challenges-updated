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

We will start with a clean slate for these challenges. The project on which we will be working is similar to the codebase you worked with until now, but now you have a new directory `/taxifare_api` and new files within the `model` project directory.

First, let's have a look at this new directory:

```bash
.
├── MANIFEST.in         # 🆕 Config file for production purpose
├── Makefile            # Good old task manager
├── README.md           # Package documentation
├── Dockerfile          # 🆕 Building instructions
├── requirements.txt    # All the dependencies you need to run the package
├── setup.py            # Package installer
├── taxifare_api        # 🆕 API directory
│   ├── __init__.py
│   └── fast.py         # 🆕 Where the API lays
├── taxifare_flow       # DAG stuff
├── taxifare_model      # ML logic
└── tests               # Your favorite 🍔
```

**❓ What's inside that new directory?**

<details>
  <summary markdown='span'>Answer</summary>

🎁 As you can see, it contains a new **module** named **`taxifare_api`** you are going to implement!

</details>
<br>

Now, navigate into the `/model` directory, have a look at the `requirements.txt`. You can see new comers:
```txt
# API
fastapi         # API framework
pytz            # Timezones management
uvicorn         # Web server
# tests
httpx           # HTTP client
pytest-asyncio  # Asynchronous I/O support for pytest
```
⚠️ Make sure perform a **clean install** of the package.

<details>
  <summary markdown='span'>❓ How?</summary>

`make reinstall_package` of course 😉

</details>

### Running the API with FastAPI and a Uvicorn server

We provide you with with a FastAPI skeleton in the `fast.py` file.

**💻 Launch the API**

<details>
  <summary markdown='span'>💡 Hint</summary>

You probably need a `uvicorn` web server..., with a 🔥 reloading...

In case you can't find the proper syntax, keep calm and look at your   `Makefile`, we provided you with a new task `run_api`.

</details>
<br>

**❓ How do you consult your running API?**

<details>
  <summary markdown='span'>Answer</summary>

💡 Your API is available on a local port, `8000` probably 👉 [http://localhost:8000](http://localhost:8000).
Go visit it!

</details>
<br>

You probably would not have seen much.
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
  <summary markdown='span'>⚡️ Kickstart pack</summary>
Here is a piece of code you can use to kickstart the implementation:

```Python
@app.get("/predict")
def predict(pickup_datetime: datetime,  # 2013-07-06 17:18:00
            pickup_longitude: float,    # -73.950655
            pickup_latitude: float,     # 40.783282
            dropoff_longitude: float,   # -73.984365
            dropoff_latitude: float,    # 40.769802
            passenger_count: int):
    pass # YOUR CODE HERE
```

</details>

<details>
  <summary markdown='span'>💡 Hints</summary>

Ask yourselves the following questions:
- How should we handle the query parameters?
- How can we re-use the `taxifare_model` package?
- How should we build `X_pred`? What does it look like?
- How to render the correct response?
</details>

<details>
  <summary markdown='span'>🍔 Food for thought</summary>

1. Investigate the data types of the query parameters, you may need to convert them into the types the model requires
1. Of course you must re-use the `taxifare_model.interface.main.pred()` or the `taxifare_model.ml_logic.registry.load_model()` functions!
1. In order to make a prediction with the trained model, you must provide a valid `X_pred` but the `key` is missing!
1. FastAPI can only render data type from the Python Standard Library, you may need to convert `y_pred` to match this requirement

</details>
<br>

**👀 Inspect your browser response 👉 ['http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2](http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2)**

**🐛 Inspect the server logs and add some `breakpoint()` to debug**

Once and _only once_ your API responds as required:
**🧪 Test your implementation with `make test_predict`**

**🚀 Commit and push your code!**

**👏 Congrats, you build your first ML predictive API!**

## Build a Docker image for our API

We now have a working **predictive API** which can be queried from our local machine.

We want to make it available to the world. In order to do that, the first step is to create a **Docker image** that contains the environment required to run the API and make it run _locally_ on Docker.

**❓ What are the 3 steps to run the API on Docker?**

<details>
  <summary markdown='span'>Answer</summary>

1. **Create** a `Dockerfile` containing the the instructions to build the API
1. **Build** the image locally on Docker
1. **Run** the API on Docker locally to check it is responding as required

</details>

### Setup

You need Docker daemon to run on your machine so you  will be able to build and run the image locally.

**💻 Launch Docker daemon**

<details>
  <summary markdown='span'>MacOSX</summary>

Launch the Docker Desktop app, you should see a whale in your menu bar.

<img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/macos-docker-desktop-running.png" width="150" alt="verify that Docker Desktop is running">
</details>

<details>
  <summary markdown='span'>Windows WSL2 & Ubuntu</summary>

``` bash
sudo service docker start
```
</details>
<br>

**✅ Check Docker daemon is up and running with `docker info` in your terminal**

A nice stack of logs should print:
<a href="https://github.com/lewagon/data-setup/raw/master/images/docker_info.png" target="_blank"><img src='https://github.com/lewagon/data-setup/raw/master/images/docker_info.png' width=150></a>


### `Dockerfile`

As a reminder, here is the `/model` directory structure:

```bash
.
├── MANIFEST.in         # 🆕 Config file for production purpose
├── Makefile            # Good old task manager
├── README.md           # Package documentation
├── Dockerfile          # 👉 Building instructions
├── requirements.txt    # All the dependencies you need to run the package
├── setup.py            # Package installer
├── taxifare_api        # ✅ API directory
│   ├── __init__.py
│   └── fast.py         # ✅ Where the API lays
├── taxifare_flow       # DAG stuff
├── taxifare_model      # ML logic
└── tests               # Your favorite 🍔
```

**❓ What are the key ingredients a `Dockerfile` needs to cook a delicious Docker image?**

<details>
  <summary markdown='span'>Answer</summary>

Here the most common instructions of good `Dockerfile`:
- `FROM`: select a base image for our image (the environment in which we will run our code), this is usually the first instruction
- `COPY`: copy files and directories inside of our image (our package and the associated files for example)
- `RUN`: execute a command **inside** of the image being built (for example, install the package dependencies)
- `CMD`: execute the **main** command that will be executed when we run our **Docker image**. There can be only one `CMD` instruction inside of a `Dockerfile`. It is usually the last instruction

</details>
<br>

**❓ What the base image should contain to build our image on top of it?**

<details>
  <summary markdown='span'>💡 Hints</summary>

Choosing an image with Python already installed could be a nice start...
</details>
<br>

**💻 Write the instructions needed to build the API image in the `Dockerfile` with the following specifications:**

- [ ] it should contain the same Python version of your virtual env
- [ ] it should contain the necessary directories from the `/model` directory to allow the API to run
- [ ] it should contain the dependencies list
- [ ] the API depencies should be installed
- [ ] the web server should be launched
- [ ] the web server should listen to the HTTP requests coming from outside the container (cf `host` parameter)
- [ ] the web server should be able listen to a specific port defined by an environment variable `$PORT` (cf `port` parameter)

<details>
  <summary markdown='span'>⚡️ Kickstart pack</summary>

Here is the skeleton of the `Dockerfile`:

```Dockerfile
FROM image
COPY api
COPY model
COPY dependencies
RUN install dependencies
CMD launch API web server
```

</details>
<br>

**❓ How would you check if the `Dockerfile` instructions will execute what you wanted?**

<details>
  <summary markdown='span'>Answer</summary>

You can't at this point! 😁 You need to build the image and check if it contains everything required to run the API. Go to the next section: Build the API image.
</details>
