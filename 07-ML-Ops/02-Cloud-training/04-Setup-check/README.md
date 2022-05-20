
[//]: # ( challenge tech stack: gcloud gsutil cloud-storage )

[//]: # ( challenge presentation )

First things first, let's make sure that your machine is ready to drive **Google Cloud Platform** ressources.

In this challenge, we will:
- Verify that your **GCP** setup is operationnal
- Discover the `gcloud` and `gsutil` **Command Line Interface** tools provided by GCP in order to drive ressources in the cloud

**🚨 💻 Install the package of the challenge with `make reinstall_package`**

💡 Remember that you can alway list the available `Makefile` commands with `make list`

[//]: # ( challenge instructions )

## Setup check

Let's make sure that your setup is operational.

First, we need to install some useful Python packages to interact from your code with GCP APIs such as [Cloud Storage](https://cloud.google.com/storage/docs/apis) and [BigQuery](https://cloud.google.com/bigquery/docs/reference/rest):

``` bash
pip install google-cloud-storage "google-cloud-bigquery<3.0.0"
```

We will now verify that:
- The `gcloud` CLI tool has access to your GCP account
- The _python_ code running on your machine has access to your GCP account

**🧪 In your terminal, run the tests with `make dev_test`**

👉 `test_setup_cli_auth`, `test_setup_key_env`, `test_setup_key_path`, `test_code_get_project` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You can head back towards the _Google Cloud Platform setup_ section of the [data setup](https://github.com/lewagon/data-setup) and in particular have a look at *Create a service account key*.

  Don't stay stuck for too long here, ask for a TA if your setup is not operational.
</details>

## The `gcloud` CLI

Let's discover the first CLI tool allowing you to drive your GCP ressources from the terminal.

The `gcloud` CLI allows you to interact with almost all of the ressources of your account (there are other dedicated commands for specific products, such as `bq` for Big Query).

Your GCP ressources are organised in **projects**. Before allocating a ressource, you need to determine to which project it will be attached.

**❓ How do you list your GCP projects ?**

Find the `gcloud` command allowing you to list your **GCP project id**.

**📝 Fill the `PROJECT` variable in the `.env` project configuration**

**🧪 Run the tests with `make dev_test`**

👉 `test_setup_project_id` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You can use the `-h` flag or the `--help` (more details) parameter in order to retrieve contextual help on the `gcloud` commands or sub commands (use `gcloud billing -h` to list the gcloud billing sub commands or `gcloud billing --help` for a more detailed help on the sub commands).

  Also note that running `gcloud` without arguments lists all the available sub commands by group.
</details>

## Cloud Storage and the `gsutil` CLI

The second CLI tool that you will use often allows you to deal with files stored in the cloud.

Files stored in the cloud on your GCP account with Cloud Storage are organised in **buckets** attached to a project.

In order to store or retrieve files from the cloud, we first need to create a bucket to work with.

**❓ How do you create a bucket ?**

Find the `gsutil` command allowing you to create a **bucket**.

**💻 Create a bucket in your GCP account**

**🧪 Run the tests with `make dev_test`**

👉 `test_setup_bucket_exists` should be ✅

Imagine you are working on a project on which several teams are collaborating. You need to be able to identify on which bucket to store your files.

**❓ How do you list the GCP buckets you have access to ?**

Find the `gsutil` command allowing you to retrieve the name of your **bucket**.

**📝 Fill the `BUCKET_NAME` variable in the `.env` project configuration**

**🧪 Run the tests with `make dev_test`**

👉 `test_setup_bucket_name` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You can also use the [Cloud Storage console](https://console.cloud.google.com/storage/) in order to verify that the bucket was created.

  Do you see how much slower than the command line the GCP console (web interface) is ?
</details>

All tests should pass! 👏
