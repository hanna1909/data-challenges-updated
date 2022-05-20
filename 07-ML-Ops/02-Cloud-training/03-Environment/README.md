
[//]: # ( challenge tech stack: direnv )

[//]: # ( challenge presentation )

In this challenge, we will discover:
- How to handle the configuration for the _WagonCab_ project
- How to load environment variables in your code and in the terminal

[//]: # ( challenge instructions )

## Configuration setup

Our goal is to be able to configure the behavior of our project based on variables defined in a `.env` project configuration file.

In order to do so, we will install the `direnv` shell extension. Its job is to locate the nearest `.env` file in the parent directory structure of the project and load its content into the environment.

<details>
  <summary markdown='span'><strong> ⚙️ macOS </strong></summary>


  ``` bash
  brew install direnv
  ```
</details>

<details>
  <summary markdown='span'><strong> ⚙️ Ubuntu (Linux or Windows WSL2) </strong></summary>


  ``` bash
  sudo apt update
  sudo apt install -y direnv
  ```
</details>

Once `direnv` is installed, we need to tell `zsh` to load `direnv` whenever it starts. This will allow `direnv` to monitor the changes in the `.env` project configuration, and to refresh the `environment variables` accordingly.

**❓ How do you configure `zsh` ?**

Edit your `~/.zshrc` with your favorite editor. The `~/.zshrc` is interpreted by `zsh` whenever a new terminal window or tab is opened or if you create a new session by running `zsh` in the terminal.

**💻 Add `direnv` to the list of plugins**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  Open the ressources files:

  ``` bash
  code ~/.zshrc
  ```

  The list of plugins is located at the start of the files and should look this this when you add `direnv`:

  ``` bash
  plugins=(git gitfast last-working-dir common-aliases zsh-syntax-highlighting history-substring-search pyenv direnv)
  ```
</details>

**💻 Start a new `zsh` window in order to load `direnv`**

## Adding configuration variables

Let's add a few configuration variables to the project. We provide a `07-ML-Ops/.env.sample` template configuration file for the project. Copy it and rename it as `07-ML-Ops/.env`.

This configuration file will be read by `direnv` and the variables it declares will be loaded into the environment.

``` bash
cp ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/.env.sample ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/.env
```

👉 We will continue to add variables to this file in the next challenges and units in order to configure further our project

## Enable the `.env` project configuration

`direnv` will not load the `.env` project configuration without asking. As a security check, you need to tell it which files are safe to load into your environment, since the environment variables allow to drive the behavior of your project and potentially much more on your machine.

**❓ How do you tell `direnv` to load your `.env` project configuration file ?**

**💻 Activate your `.env` project configuration file using the `direnv` command**

**🧪 In your terminal, run the tests with `make dev_test`**

👉 `test_environment_dataset_size` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You can retrieve info on how `direnv` works with:

  ``` bash
  direnv --help
  ```

  In order to activate your `.env` project configuration file:

  ``` bash
  cd ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops
  direnv allow .
  ```
</details>

## Update your `.env` project configuration

From now on, whenever you need to update the behavior of the project, you will be able to change its parameters by simply editing the `.env` project configuration.

**❓ How do you identify the location of the `.env` project configuration loaded by `direnv` ?**

👉 You can list the directory where the `.env` is located with this command:

``` bash
echo $DIRENV_DIR
```

**📝 Fill the `HELLO` variable in the `.env` project configuration with the value `world !`**

**🧪 Run the tests with `make dev_test`**

👉 `test_environment_hello` should be ✅

Let's store something a little more useful in the configuration...

Remember how we want to store our datasets in a single location for all the challenges ?

This location is:

``` bash
~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/data
```

**📝 Fill the `LOCAL_DATA_PATH` variable in the `.env` project configuration with this path**

**🧪 Run the tests with `make dev_test`**

👉 `test_local_data_path` should be ✅

Last, let's fill the path to the centralized registry directory that will store our trained models, params and metrics.

Its location is:

``` bash
~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/registry
```

**📝 Fill the `LOCAL_REGISTRY_PATH` variable in the `.env` project configuration with this path**

**🧪 Run the tests with `make dev_test`**

👉 `test_local_registry_path` should be ✅

🏁 You are ready to go!
