
[//]: # ( challenge tech stack: direnv )

[//]: # ( challenge presentation )

In this challenge, we will discover:
- How to handle the configuration for the _WagonCab_ project through a `.env` file
- How to load environment variables in your _code_ 📝 and in the _terminal_ 💻

🚨 You will need to create and customize a `.env` file at the start of each challenge in the module

👉 Do not worry, we provide a template and will remind you to do so

[//]: # ( challenge instructions )

## Configuration setup

Our goal is to be able to configure the behavior of our _package_ 📦 depending on the value of the variables defined in a `.env` project configuration file.

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

The `zsh` resource file (`~/.zshrc`) contains scripts and parameters for `zsh` and is interpreted whenever a new _terminal_ window or tab is opened, or when you create a new [shell](https://en.wikipedia.org/wiki/Shell_(computing)) session by running `zsh` in the terminal.

You need to update your `~/.zshrc` file in order to tell it to load `direnv`.

**💻 Add `direnv` to the list of `zsh` plugins**

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  Open the resources files:

  ``` bash
  code ~/.zshrc
  ```

  The list of plugins is located at the start of the files and should look this this when you add `direnv`:

  ``` bash
  plugins=(git gitfast last-working-dir common-aliases zsh-syntax-highlighting history-substring-search pyenv direnv)
  ```
</details>

**💻 Start a new `zsh` window in order to load `direnv`**

👉 At this point `direnv` is still not able to load anything: there is no `.env` file

## Add a `.env` configuration file

We provide a `.env.sample` template configuration file for each of the challenges. Copy it and rename it as `.env`.

This configuration file will be read by `direnv` and the variables it declares will be loaded into the environment.

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

<details>
  <summary markdown='span'><strong> 💡 `direnv` does not load the content of my `.env` </strong></summary>


  Try to refresh `direnv` with `direnv reload`.
</details>

Let's store something a little more useful in the configuration...

Remember how we moved our datasets to a single location for all the challenges ?

The location of the data shared by all the challenges is:

``` bash
~/.lewagon/mlops/data
```

**📝 Fill the `LOCAL_DATA_PATH` variable in the `.env` project configuration with this path**

**🧪 Run the tests with `make dev_test`**

👉 `test_local_data_path` should be ✅

Last, let's fill the path to the shared `training_outputs` directory that will store our trained models, params and metrics:

``` bash
~/.lewagon/mlops/training_outputs
```

**📝 Fill the `LOCAL_REGISTRY_PATH` variable in the `.env` project configuration with this path**

**🧪 Run the tests with `make dev_test`**

👉 `test_local_registry_path` should be ✅

🤔 Are all the tests still not green ? Remember to always `make reinstall_package` so that the code that you use is the one of the challenge in which you sit

<details>
  <summary markdown='span'><strong> 💡 How can I make sure that `direnv` loaded the variables in my `.env` without running my code ? </strong></summary>


  This is the time to use the commands provided in the `Makefile` and verify that the variables are correctly loaded into the environment whenever you feel like it:

  ``` bash
  make show_env
  ```

  👉 How does that work ? Very simple: the `show_env` command in the `Makefile` just runs an `echo` (a `print` in the _terminal_) of the content of the varialbes of the project loaded by `direnv`
</details>

🏁 You are ready to go!
