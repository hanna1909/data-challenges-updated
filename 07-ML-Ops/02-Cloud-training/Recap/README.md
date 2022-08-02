
[//]: # ( challenge tech stack: vertex-ai workbench )

[//]: # ( challenge instructions )

## Vertex AI Workbench

Let's explore **Vertex AI Workbench** as an alternative to **Compute Engine** for the model training.

_Vertex AI Workbench_ provides managed virtual machines allowing to run ML code without having to configure precisely the environment for the code:
- _User managed notebooks_ provides a customisable environment and allows to specify package versions
- _Managed notebooks_ uses custom containers, can be extended to read or write to big query or cloud storage, and can be scheduled for run

### Create a workbench instance

Create a workbench instance:
- [Vertex AI Workbench](https://console.cloud.google.com/vertex-ai/workbench)
- _USER-MANAGED NOTEBOOKS_ / _NEW NOTEBOOK_
- _TensorFlow Enterprise_ / _TensorFlow Enterprise 2.8 (with LTS)_ / _Without GPUs_
- Notebook name: _cloud-training-recap_
- _ADVANCED OPTIONS_ / Operating System: _Ubuntu 20.04_
- _CREATE_

👉 The workbench should be ready in a couple of minutes

Open the virtual machine
- _OPEN JUPYTERLAB_
- Install [gh](https://github.com/cli/cli/blob/trunk/docs/install_linux.md) for _Ubuntu_

### Install zsh and oh-my-zsh

Install zsh:

``` bash
sudo apt-get install zsh
```

Install oh-my-zsh:

``` bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### Authenticate to GitHub 1/2

Go to workbench instance and open a terminal.

Run the `gh auth login` command:
- Account: `GitHub.com`
- Protocol: `HTTPS`
- Authenticate Git with your GitHub credentials: `Yes`
- Authentication method: `Paste an authentication token`

### Create a GitHub token

Create a GitHub token to allow the workbench to access to your account:
- [GitHub Tokens](https://github.com/settings/tokens)
- _Generate new token_
- Fill _Note_ with a meaningul name: _Vertex AI Workbench token_
- Check the scopes: 'repo', 'read:org', 'workflow'
- _Generate token_
- Copy the token (you will not be able to retrieve it later)

### Authenticate to GitHub 2/2

In workbench instance terminal:
- Paste the token in the Vertex AI instance terminal

### Clone your project repo

Clone your repo using an `HTTPS` URL:

``` bash
git clone https://github.com/gmanchon/cloud-data-recap-dm
cd cloud-data-recap-dm
cp .env.sample .env
nano .env
```

Edit the project configuration file:
- Set the data source as `DATA_SOURCE="big query"`
- Exit and save `Ctrl + X`, `Y`, `Enter`

Install direnv:

``` bash
curl -sfL https://direnv.net/install.sh | bash
eval "$(direnv hook zsh)"
direnv allow .
```

Install package:

``` bash
pip install -e .
mkdir -p training_outputs/params training_outputs/metrics training_outputs/models
```

Run the preprocess and training:

``` bash
make run_preprocess run_train
tree training_outputs
```

### New workbench terminal

Manually hook direnv:

``` bash
eval "$(direnv hook zsh)"
```

### Handling the `.env` in jupyter lab

The easiest solution is to manually define the environment variables from python:

``` python
import os

os.environ["DATASET_SIZE"] = "10k"
os.environ["VALIDATION_DATASET_SIZE"] = "10k"
os.environ["CHUNK_SIZE"] = "2000"
os.environ["DATA_SOURCE"] = "local"
os.environ["MODEL_TARGET"] = "local"
os.environ["PREFECT_BACKEND"] = "local"
os.environ["PROJECT"] = "le-wagon-dsa"
```

## Compute Engine vs Vertex AI Workbench

In _Compute Engine_ we can see that _Vertex AI Workbench_ uses a _Compute Engine_ instance behind the scenes:

<img src='https://wagon-public-datasets.s3.eu-west-1.amazonaws.com/data-science-images/07-ML-OPS/mlops/vertex-ai-compute-engine.png'>
