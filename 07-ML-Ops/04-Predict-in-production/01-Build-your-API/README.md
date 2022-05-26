[//]: # ( challenge tech stack: fastapi uvicorn )

[//]: # ( challenge instructions )

## Objective

Use **FastAPI** in order to create an API for your model.

Run that API on your machine. Then put it in production.

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
├── Dockerfile          # 🆕 Building instructions
├── MANIFEST.in         # 🆕 Config file for production purpose
├── Makefile            # Good old task manager
├── README.md           # Package documentation
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

Now, navigate into the `/model` directory, have a look at the `requirements.txt`. You can see new comers:

``` bash
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

In case you can't find the proper syntax, keep calm and look at your `Makefile`, we provided you with a new task `run_api`.

</details>

**❓ How do you consult your running API?**

<details>
  <summary markdown='span'>Answer</summary>

💡 Your API is available on a local port, `8000` probably 👉 [http://localhost:8000](http://localhost:8000).
Go visit it!

</details>

You have probably not seen much.

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
**🧪 Test your implementation with `make test_api_root`**

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
  <summary markdown='span'>⚙️ Configuration</summary>

Have you put a trained model in _Production_ in mlflow? If not, you can use the following configuration:

``` bash
MLFLOW_TRACKING_URI=https://mlflow.lewagon.ai
MLFLOW_EXPERIMENT=taxifare_experiment_recap
MLFLOW_MODEL_NAME=my_taxifare
```
</details>

<details>
  <summary markdown='span'>🍔 Food for thought</summary>

1. Investigate the data types of the query parameters, you may need to convert them into the types the model requires
1. Of course you must re-use the `taxifare_model.interface.main.pred()` or the `taxifare_model.ml_logic.registry.load_model()` functions!
1. In order to make a prediction with the trained model, you must provide a valid `X_pred` but the `key` is missing!
1. FastAPI can only render data type from the Python Standard Library, you may need to convert `y_pred` to match this requirement

</details>

**👀 Inspect your browser response 👉 ['http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2](http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2)**

**🐛 Inspect the server logs and add some `breakpoint()` to debug**

Once and _only once_ your API responds as required:
**🧪 Test your implementation with `make test_api_predict`**

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

**❓ What the base image should contain to build our image on top of it?**

<details>
  <summary markdown='span'>💡 Hints</summary>

Choosing an image with Python already installed could be a nice start...
</details>

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

**❓ How would you check if the `Dockerfile` instructions will execute what you wanted?**

<details>
  <summary markdown='span'>Answer</summary>

You can't at this point! 😁 You need to build the image and check if it contains everything required to run the API. Go to the next section: Build the API image.
</details>

### Build the API image

Now is the time to **build** the API image on Docker so you can check if it satisfies the requirements and be able to run it on Docker.

**❓ How do you build an image with Docker?**

<details>
  <summary markdown='span'>Answer</summary>

Make sure you are in the directory of the `Dockefile` then:
```bash
docker build --tag=image-name .
```
where `image-name` is the name of your image.
</details>

**💻 Choose a meaningful name for the API image then build it**

Once built, the image should be visible in the list of images built with the following command:

``` bash
docker images
```

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/docker_images.png'>

**🕵️‍♀️ The image you are looking for does not appear in the list? Ask for help 🙋‍♂️**

### Check the API image

Now the image is built let's check it satisfies the specifications to run the predictive API. Docker comes with a handy command to **iteractively** communicate with the shell of the image:

``` bash
docker run -it -e PORT=8000 -p 8000:8000 image-name sh
```

<details>
  <summary markdown='span'>🤖 Decrypt</summary>

- `docker run image-name` runs the image name `image-name`
- `-it` enable the intercative mode
- `-e PORT=8000` specify the environment variable `$PORT` the image should listen to
- `sh` launch a shell console
</details>

A shell console should open, you are inside the image 👏.

**💻 Check the image is correctly set up:**

- [ ] The python version is the same as your virtual env
- [ ] Presence of the `/taxifare_api` and `taxifare_model` directories
- [ ] Presence of the `requirements.txt`
- [ ] The dependencies are all installed

<details>
  <summary markdown='span'>🙈 Solution</summary>

- `python --version` to check the Python version
- `ls` to check the presence of the files and directories
- `pip list` to check the requirements are installed
</details>

Exit the terminal and stop the container at any moment with:

``` bash
exit
```

**✅ ❌ All good? If something is missing, you  would probably need to fix your `Dockerfile` and re-build the image again**

### Run the API image

In the previous section you learned how to interact with the image shell. Now is the time to run the predictive API image and
test if the API responds as it should.

**💻 Run the image**

<details>
  <summary markdown='span'>💡 Hints</summary>

You should probably remove the interactivity mode and forget the `sh` command...
</details>

**🐛 Unless you fing the correct command to run the image, it is probably crashing with errors involving environment variable.**

**❓ What is the difference between your local environment and image environment? 💬 Discuss with your buddy.**

<details>
  <summary markdown='span'>Answer</summary>

There is **no** `.env` in the image!!! The image has **no** access to the environment variables 😈
</details>

**💻 Using the `docker run --help` documentation, adapt the run command so the `.env` is send to the image**

<details>
  <summary markdown='span'>🙈 Solution</summary>

The `--env-file` parameter to the rescue!

```bash
docker run -e PORT=8000 -p 8000:8000 --env-file path/to/.env image_name
```
</details>

**❓ How would check the image runs correctly?**

<details>
  <summary markdown='span'>💡 Hints</summary>

The API should respond in your browser, go visit it!

Also you can check the image runs with:
``` bash
docker ps
```
</details>

It's Alive! 😱 🎉

**👀 Inspect your browser response 👉 [http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2](http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2)**

**👏 Congrats, you build your first ML predictive API inside a Docker container!**

## Deploy the API

Now we have built a **predictive API** Docker image that we are able to run on our local machine, we are 2 steps away from deploying:
- Push the **Docker image** to **Google Container Registry**
- Deploy the image on **Google Cloud Run** so that it gets instantiated into a **Docker container**


### Push our prediction API image to Google Container Registry

**❓ What is the purpose of Google Container Registry ?**

<details>
  <summary markdown='span'>Answer</summary>

**Google Container Registry** is a service storing Docker images on the cloud with the purpose of allowing **Cloud Run** or **Kubernetes Engine** to serve them.

It is in a way similar to **GitHub** allowing you to store your git repositories in the cloud (except for the lack of a dedicated user interface and additional services such as `forks` and `pull requests`).

</details>

#### Setup

First, let's make sure to enable [Google Container Registry API](https://console.cloud.google.com/flows/enableapi?apiid=containerregistry.googleapis.com&redirect=https://cloud.google.com/container-registry/docs/quickstart) for your project in GCP.

Once this is done, let's ensure that your GCP credentials are correctly registered for the command line.

``` bash
gcloud auth list
```

If your account is not listed then you have to authenticate:

``` bash
gcloud auth login
```

Now let's configure the `gcloud` command for the usage of Docker.

``` bash
gcloud auth configure-docker
```

And verify your config. You should see your GCP account and default project.

``` bash
gcloud config list
```

Define an environment variable for the name of your project.

``` bash
export PROJECT_ID=replace-with-your-gcloud-project-id
echo $PROJECT_ID # print the PROJECT_ID
gcloud config set project $PROJECT_ID
```

And an environment variable for the name of your docker image.
This environment variable will be used accross the following commands.

``` bash
export DOCKER_IMAGE_NAME=define-some-container-image-name
echo $DOCKER_IMAGE_NAME
```

#### Build and push the image on GCR

Now we are going to build our image again.
This should be pretty fast since Docker is pretty smart and is going to reuse all the building blocks used previously in order to build the prediction API image.

``` bash
docker build -t eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME .
```

Again, let's make sure that our image runs correctly, so that we avoid spending the time on pushing an image that is not working to the cloud.

``` bash
docker run -e PORT=8000 -p 8000:8000 --env-file path/to/.env eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME
```
Visit [http://localhost:8000/](http://localhost:8000/) and check the API is running as expected.

We can now push our image to Google Container Registry.

``` bash
docker push eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME
```

The image should be visible in the GCP console [here](https://console.cloud.google.com/gcr/).

### Deploy the Container Registry image to Google Cloud Run

**❓ What is the purpose of Cloud Run?**
<details>
  <summary markdown='span'>Answer</summary>

Cloud Run will instantiate the image into a container and run the `CMD` instruction inside of the `Dockerfile` of the image. This last step will start the `uvicorn` server serving our **predictive API** to the world 🌍

</details>

Let's run one last command 🤞

``` bash
gcloud run deploy --image eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME --platform managed --region europe-west1
```

After confirmation, you should see a similar output indicating that the service is live 🎉

``` txt
Service name (wagon-data-tpl-image):
Allow unauthenticated invocations to [wagon-data-tpl-image] (y/N)?  y

Deploying container to Cloud Run service [wagon-data-tpl-image] in project [le-wagon-data] region [europe-west1]
✓ Deploying new service... Done.
  ✓ Creating Revision... Revision deployment finished. Waiting for health check to begin.
  ✓ Routing traffic...
  ✓ Setting IAM Policy...
Done.
Service [wagon-data-tpl-image] revision [wagon-data-tpl-image-00001-kup] has been deployed and is serving 100 percent of traffic.
Service URL: https://wagon-data-tpl-image-xi54eseqrq-ew.a.run.app
```

Any developer in the world 🌍 is now able to browse to the deployed url and make a prediction using the API 🤖!

⚠️ Keep in mind that you pay for the service as long as it is up 💸

**👏 Congrats, you deployed your first ML predictive API!**

## Once you are done with Docker...

You may stop (or kill) the image...

``` bash
docker stop 152e5b79177b  # ⚠️ use the correct CONTAINER ID
docker kill 152e5b79177b  # ☢️ only if the image refuses to stop (did someone create an ∞ loop?)
```
Remember to stop the Docker daemon in order to free ressources on your machine once you are done using it...

<details>
  <summary markdown='span'>MacOSX</summary>

Stop the `Docker.app` with **Quit Docker Desktop** in the menu ba
</details>

<details>
  <summary markdown='span'>Windows WSL2/Ubuntu</summary>

``` bash
sudo service docker stop
```
</details>
