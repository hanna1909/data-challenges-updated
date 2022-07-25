
[//]: # ( challenge tech stack: compute-engine gcloud )

[//]: # ( challenge presentation )

We have stored the training and validation datasets in the cloud in our first data warehouse. We updated the package in order to be able to consume and update the data by chunks from the data warehouse. We are ready to move the training of the model itself to the cloud.

In this challenge, we will discover the third pillar product of the **Google Cloud Platform** suite:

🏍 **Compute Engine**, which provides *Virtual Machines*, will allow us to do the actual training in the cloud

<details>
  <summary markdown='span'><strong> 🔎 More on Compute Engine </strong></summary>


  Compute Engine is the service that powers behind the scenes most of the GCP products that require computing capacity.

  It is leveraged by almost all the GCP products. This is why you often see allocated Compute Engine VM instances when you use other GCP products. This is the case for Cloud Run, which you will discover in the second next unit.

  Compute Engine allows us to allocate a custom tailored virtual machine that we can put to sleep when we do not need it anymore. We can create a VM with custom processing power, memory, and disk space, for the duration that we wish.

  It is hard to evaluate properly how to size a machine for a training beforehands. You will have to balance the cost and the capacity of the machine, experiment with the dataset size and observe the training time in order to make up your mind. And possibly opt for [using a GPU](https://kitt.lewagon.com/knowledge/tutorials/vertex_api) or a TPU depending on your goal.
</details>

**💻 As always, first install the package of the challenge with `make reinstall_package`**

**💻 You know the `.env` drill (_copy_ the `.env.sample`, _fill_ the `.env`, _allow_ `direnv`)**

[//]: # ( challenge instructions )

## Enable the Compute Engine service

In GCP, many services are not enabled by default. The service to activate in order to use _virtual machines_ is **Compute Engine**.

**❓ How do you enable a GCP service ?**

Find the `gcloud` command allowing you to enable a **service**.

**💻 Enable the Compute Engine service**

**🧪 Run the tests with `make dev_test`**

👉 `test_cloud_training_compute_api_enabled` should be ✅

## Create your first Virtual Machine

The `taxifare_model` package is ready to train on a machine in the cloud. Let's create our first *Virtual Machine* instance!

**❓ How do you create a virtual machine ?**

Head towards the GCP console [Compute Engine](https://console.cloud.google.com/compute) page. The console will allow you to explore easilly the options available. Make sure to create an **Ubuntu** instance (read this _How to_, and have a look at the _Hint_).

<details>
  <summary markdown='span'><strong> 🗺 How to configure your VM instance </strong></summary>


  Let's explore the options available. The top right of the interface gives you a monthly estimate of the cost for the selected parameters if the VM remains on all the time.

  The basic options should be enough for what we want to do now, except for one: we want to choose the operating system that the VM instance will be running.

  Go to the *Boot disk* section, *CHANGE* the *Operating System* to **Ubuntu** and select the latest **Ubuntu xx.xx LTS** (Long Term Support) version.

  Ubuntu is the familly of operating systems that will ressemble the most the configuration on your machine following the [Le Wagon setup](https://github.com/lewagon/data-setup). Whether you are on a Mac, using Windows WSL2 or on Linux. Selecting this option will allow you to play with a remote machine using the commands you are already familiar with.
</details>

**💻 Create a VM instance and fill the `INSTANCE` variable in the `.env` project configuration**

**🧪 Run the tests with `make dev_test`**

👉 `test_cloud_training_create_vm` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  In the future, when you know exactly what type of VM you want to create, you will be able to use the `gcloud compute instances` commands if you want to do everything from the command line. For example:

  ``` bash
  INSTANCE=taxi-instance
  IMAGE_PROJECT=ubuntu-os-cloud
  IMAGE_FAMILY=ubuntu-2110

  gcloud compute instances create ${INSTANCE} --image-project=${IMAGE_PROJECT} --image-family=${IMAGE_FAMILY}
  ```
</details>

**❓ How switch ON/OFF your VM ?**

You can easily start and stop a vm instance from the GCP console, which allows to see which instances are running.

<a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-vm-start.png"><img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-vm-start.png" width="150" alt="gce vm start"></a>

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  A faster way to start and stop your virtual machine is to use the command line. The commands still take some time to complete, but you do not have to navigate through the GCP console interface.

  Have a look at the `gcloud compute instances` commands in order to start, stop or list your instances:

  ``` bash
  INSTANCE=taxi-instance

  gcloud compute instances stop ${INSTANCE}
  gcloud compute instances list
  gcloud compute instances start ${INSTANCE}
  ```
</details>

🚨 Computing power does not grow on trees 🌳, do not forget to switch the VM off whenever you stop using it 💸

## Setup your VM

You have access at arms length to virtually unlimited computing power. Easilly switched on and off. Ready to help with trainings or any tasks.

**❓ How do you connect to the VM ?**

The GCP console allows you to connect to the VM instance through a web interface:

<a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-vm-ssh.png"><img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-vm-ssh.png" width="150" alt="gce vm ssh"></a><a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-console-ssh.png"><img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-console-ssh.png" width="120" alt="gce console ssh"></a>

You can disconnect by typing `exit` or closing the window.

A nice alternative is to connect to the virtual machine right from your command line 🤩

<a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-ssh.png"><img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-ssh.png" width="150" alt="gce ssh"></a>

All you need to do is to `gcloud compute ssh` on a running instance and to run `exit` when you want to disconnect 🎉

``` bash
INSTANCE=taxi-instance

gcloud compute ssh ${INSTANCE}
```

<details>
  <summary markdown='span'><strong> 💡 Connecting with a different user </strong></summary>


  You can change the user the web interface connects with if you need to:

  <a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-web-ssh-switch-login.png"><img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-web-ssh-switch-login.png" width="120" alt="gce web ssh switch login"></a>

  You can also specify the user to connect with when using the command line:

  ``` bash
  gcloud compute ssh ${USERNAME}@${INSTANCE}
  ```
</details>

<details>
  <summary markdown='span'><strong> 💡 Error 22 </strong></summary>


  If you encounter a `port 22: Connection refused` error, just wait a little more for the VM instance to complete its startup.

  Just run `pwd` or `hostname` if you ever wonder on which machine you are running your commands.
</details>

You have allocated a _virtual machine_ with custom characteristics able to run tasks in the cloud. And you are able to connect to it using `ssh` and run commands as you do on your local machine. You can drive the machine remotely using the _cli_, but what do you need to do in order to be able to run your code on it ? You need to create an execution environment for your code, install python and the package dependencies for your code.

You are a step away from being able to train your model: you need a development environment to have a data science ready vm 🧪

**❓ How do you setup the VM to run your python code ?**

Let's run a light version of the [Le Wagon setup](https://github.com/lewagon/data-setup).

**💻 Connect to your VM instance and run the commands of the following sections**

<details>
  <summary markdown='span'><strong> ⚙️ <code>zsh</code> and <code>omz</code> </strong></summary>


  The **zsh** shell and its **Oh My Zsh** framework are the _command line interface_ configuration you are already familiar with. Accept to make zsh the default shell when prompted to.

  ``` bash
  sudo apt update
  sudo apt install -y zsh
  sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
  ```
</details>

👉 Now the _cli_ of the remote machine starts to look a little more like the _cli_ of your local machine

<details>
  <summary markdown='span'><strong> ⚙️ <code>pyenv</code> and <code>pyenv-virtualenv</code> </strong></summary>


  Clone the repos:

  ``` bash
  git clone https://github.com/pyenv/pyenv.git ~/.pyenv
  git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
  ```

  Add `pyenv`, `ssh-agent` and `direnv` to the list of `zsh` plugins in the line `plugins=(git)` in the `~/.zshrc`: you should have `plugins=(git pyenv ssh-agent direnv)`. Then exit and save (`Ctrl + X`, `Y`, `Enter`) and save:

  ``` bash
  nano ~/.zshrc
  ```

  Make sure that the modifications are saved:

  ``` bash
  cat ~/.zshrc | grep "plugins="
  ```

  Add the pyenv initialization script to your `~/.zprofile`:

  ``` bash
  cat << EOF >> ~/.zprofile
  export PYENV_ROOT="\$HOME/.pyenv"
  export PATH="\$PYENV_ROOT/bin:\$PATH"
  eval "\$(pyenv init --path)"
  EOF
  ```
</details>

👉 Now we are ready to install python

<details>
  <summary markdown='span'><strong> ⚙️ <code>python</code> </strong></summary>


  Add dependencies required to build python:

  ``` bash
  sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
  python-dev python3-dev
  ```

  ℹ️ If a window pops up to ask you which services to restart, just press *Enter*:

  <a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-apt-services-restart.png"><img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-apt-services-restart.png" width="150" alt="gce apt services restart"></a>

  Now we need to start a new user session so that the updates in the `~/.zshrc` and `~/.zprofile` are taken into account.

  Exit the _virtual machine_: you need to `exit` from `zsh` (since you just installed it), then `exit` from the _vm_:

  ``` bash
  exit
  exit
  ```

  Then reconnect:

  ``` bash
  gcloud compute ssh ${INSTANCE}
  ```

  Install python `3.8.12` and create a `lewagon` virtual env. This can take a while and look like it is stuck, but it is not:

  ``` bash
  pyenv install 3.8.12
  pyenv global 3.8.12
  pyenv virtualenv 3.8.12 lewagon
  pyenv global lewagon
  ```
</details>

👉 See how you can easily experiment with new environment configurations on a recyclable _virtual machine_ without putting your local development environment at risk

<details>
  <summary markdown='span'><strong> ⚙️ <code>git</code> authentication to GitHub </strong></summary>


  Git will be pretty handy to share our code between the vm and your machine. Let's copy your git credentials from your machine to the _vm_:

  Copy your private key 🔑 to the _vm_ in order to allow it to access to your GitHub account.

  ⚠️ Run this single command on your machine, not in the vm ⚠️

  ``` bash
  INSTANCE=taxi-instance

  gcloud compute scp ~/.ssh/id_ed25519 ${INSTANCE}:~/.ssh/
  ```

  ⚠️ Then resume to running other commands in the vm ⚠️

  Register the key you just copied:

  ``` bash
  ssh-add ~/.ssh/id_ed25519
  ```

  Enter your *passphrase* if asked to.
</details>

👉 You are now able to interact with your **GitHub** account from your the _virtual machine_

<details>
  <summary markdown='span'><strong> ⚙️ <em>python</em> code authentication to GCP </strong></summary>


  The code of your package needs to be able to access to your Big Query data warehouse.

  In order to do that we will copy your service account json key file 🔑 to the vm. A more secure option is to create a dedicated *service account* with the appropriate access for your app and upload its json key file to the vm.

  ⚠️ Run this single command on your machine, not in the vm ⚠️

  ``` bash
  INSTANCE=taxi-instance

  gcloud compute scp $GOOGLE_APPLICATION_CREDENTIALS ${INSTANCE}:~/.ssh/
  gcloud compute ssh ${INSTANCE} --command "echo 'export GOOGLE_APPLICATION_CREDENTIALS=~/.ssh/$(basename $GOOGLE_APPLICATION_CREDENTIALS)' >> ~/.zshrc"
  ```

  ⚠️ Then resume to running other commands in the vm ⚠️

  Reload your `~/.zshrc`:

  ``` bash
  source ~/.zshrc
  ```

  Let's verify that python code can now access your GCP resources. First install some packages:

  ``` bash
  pip install google-cloud-storage
  ````

  Then [run python code from the _cli_](https://stackoverflow.com/questions/3987041/run-function-from-the-command-line). This should list your GCP projects:

  ``` bash
  python -c "from google.cloud import storage; \
      buckets = storage.Client().list_buckets(); \
      [print(b.name) for b in buckets]"
  ```

</details>

👉 That's it 🎉

Your _vm_ is now fully operational with:
- An environment (python + package dependencies) to run your code
- The credentials to connect to your _GitHub_ account
- The credentials to connect to your _GCP_ account

The only thing that is missing is the code of your project... Let's run a few tests before we install it.

**🧪 Run the tests with `make dev_test`**

👉 `test_cloud_training_default_shell`, `test_cloud_training_pyenv`, `test_cloud_training_python_version` and `test_cloud_training_list_projects` should be ✅

Your vm is now a data science beast 🔥

<details>
  <summary markdown='span'><strong> 🔎 Make a generic data science setup </strong></summary>


  You could decide to proceed with the rest of the [Le Wagon setup](https://github.com/lewagon/data-setup) and install all the packages of the bootcamp on your vm:

  ``` bash
  pip install -U pip
  pip install -r https://raw.githubusercontent.com/lewagon/data-setup/master/specs/releases/linux.txt
  ```

  Keep in mind that, if you did not configure the available disk space, by default the vm will not have enough storage for several virtual environments.
</details>

## Train in the cloud

Let's run your first training in the cloud!

**❓ How do you setup and run your project in the virtual machine ?**

**💻 Clone your package, install its requirements, and run the training**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You can copy your code to the vm by cloning your GitHub project with this syntax (adapt the name of your GitHub repository):

  ``` bash
  git clone git@github.com:<user.github_nickname>/repository_name
  ```

  Enter the directory of your package (adapt the command):

  ``` bash
  cd <path/to/the/package/model/dir>
  ```

  Create directories to save the model to:

  ``` bash
  mkdir -p data
  mkdir -p training_outputs/models
  mkdir -p training_outputs/params
  mkdir -p training_outputs/metrics
  ```

  Create a `.env` file with all required parameters to drive your package:

  ``` bash
  cp .env.sample .env
  ```

  Fill the content of the `.env` (complete the missing values):

  ``` bash
  nano .env
  ```

  ``` bash
  DATA_SOURCE=big query
  LOCAL_DATA_PATH=data
  LOCAL_REGISTRY_PATH=training_outputs
  ```

  Install `direnv` to load your `.env`:

  ``` bash
  sudo apt update
  sudo apt install -y direnv
  ```

  ℹ️ If a window pops up to ask you which services to restart, just press *Enter*.

  Disconnect from the _vm_ then reconnect (so that `direnv` works):

  ``` bash
  exit
  ```

  ``` bash
  gcloud compute ssh ${INSTANCE}
  ```

  Allow your `.envrc`:

  ``` bash
  direnv allow .
  ```

  Remove the existing local environment:

  ``` bash
  rm .python-version
  ```

  Install the dependencies of the package:

  ``` bash
  pip install pyarrow tensorflow  # this should be in your requirements.txt
  pip install -r requirements.txt
  ```

  And run the training!

  ``` bash
  make run_model  # python -m taxifare_model.interface.main
  ```
</details>

<a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-train-ssh.png"><img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-train-ssh.png" width="150" alt="gce train ssh"></a><a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-train-web-ssh.png"><img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gce-train-web-ssh.png" width="120" alt="gce train web ssh"></a>

You have trained your model in the cloud 🎉

... You can switch the vm off 🌒
