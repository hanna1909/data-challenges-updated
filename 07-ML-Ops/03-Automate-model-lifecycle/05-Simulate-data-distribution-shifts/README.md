
[//]: # ( challenge tech stack: )

**💻 Install the package of the current challenge with `make reinstall_package`**

**💻 Do not forget to handle your `.env` file (_copy_ the `.env.sample`, _fill_ the `.env`, _allow_ `direnv`)**

[//]: # ( challenge instructions )

The `taxifare_flow` package is not ready for production. But before pushing it live, we want to make sure that everything works fine when running a complete lifecycle on several iterations of new incomings data.

How can we do that ? 🤔

The data engineer of the WagonCab team has an idea 💡

They provide you with a few commands of their own crafting allowing to inject new data iteratively in your data source, either on your local machine or in **Big Query**.

Now you will be able to run several full model lifecycles and see how the performance of your model evolves over time.

## Retrieve new data

In order to run one lifecycle after the next, the commands provided by the data engineer will allow you to inject at will new data in your data source.

But how do you avoid to retrain your model on data it has already seen ?

❓ **How do you know which data is new in your data source ?**

The idea is to store in mlflow along with the training parameters the index of the last data row the model has seen during the latest training.

Luckily the tech team already though of this and the `first_row` and `row_count` parameters are already stored in mlflow on each training.

They even went as far as to provide you with a **mlflow** database schema in order to allow you to retrieve the data you are looking for.

<a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/mlflow-tables.png"><img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/mlflow-tables.png" width="150" alt="mlflow tables"></a>

And because they are very kind they also hand you a small piece of paper where the secret access codes for a read only account to the database are written in cypher:

``` bash
MLFLOW_DB_USER=taxifare_readonly
MLFLOW_DB_PASSWORD=m4e7dbNPDPg8tNR2Br36NgUGd3
MLFLOW_DB_HOSTNAME=wagon-mlflo-1768.postgresql.a.osc-fr1.scalingo-dbs.com
MLFLOW_DB_PORT=37750
MLFLOW_DB_NAME=wagon_mlflo_1768
```

Edit your `.env` project configuration file and add those variables in order to be able to use them in your code.

Once the codes are in your `.env`, find an appropriate way to destroy the small piece of paper 💣 🧨 💥 🔥

**📝 Fill the `MLFLOW_DB_USER`, `MLFLOW_DB_PASSWORD`, `MLFLOW_DB_HOSTNAME`, `MLFLOW_DB_PORT` and `MLFLOW_DB_NAME` variables in the `.env` project configuration**

**🧪 Run the tests with `make dev_test`**

👉 `test_shifts_parameters` should be ✅

Now heads back towards the code of the `taxifare_model` package and fill the function that retrieves the index of the latest row having been trained by the model (the function should return `0` if no training was ever done).

❓ **How do retrieve the index of the latest trained row ?**

Use the `first_row` and `row_count` parameters in the mlflow database in order to process the index of the latest trained row.

**💻 Complete the `get_latest_trained_row` function in `taxifare_model.ml_logic` module**

**🧪 Run the tests with `make dev_test`**

👉 `test_shifts_get_latest_trained_row` should be ✅

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>


  You can have a look at the structure of the database using **DBeaver**. Remember that `make show_env` will allow you to retrieve easily the parameters for the read only account to connect to the database. The database used by mlflow is a **Postgres** database (you need to specify the type of connection to create when using _DBeaver_).

  Another option is to use your teammate the CLI and make use of the `psql` command (for _Postgres_, you guessed it).

  Let's add a new environment variable to your `.env` project configuration. This will help you connect to the database.

  ``` bash
  MLFLOW_TRACKING_DB=postgresql://$MLFLOW_DB_USER:$MLFLOW_DB_PASSWORD@$MLFLOW_DB_HOSTNAME:$MLFLOW_DB_PORT/$MLFLOW_DB_NAME
  ```

  Since you already have all the variables filled in the `.env` for the database connection, you can query the content of the database with the following command:

  ``` bash
  psql $MLFLOW_TRACKING_DB
  ```

  No `psql` command in your setup ? Head towards the [Le Wagon web setup](https://github.com/lewagon/setup) _Postgres_ section:
  - [macOS](https://github.com/lewagon/setup/blob/master/macos.md#postgresql)
  - [Ubuntu (Linux or Windows WSL2)](https://github.com/lewagon/setup/blob/master/ubuntu.md#postgresql)

  Where do you go from there ?

  Query the list of tables:

  ``` sql
  \dt
  ```

  Consult the schema of a table:

  ``` sql
  \d runs
  ```

  Or run any regular SQL query:

  ``` sql
  SELECT * FROM runs;  -- see all the runs of your teammates
  ```

  Not unlike every other command, `psql` also supports the `exit` command...
</details>

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

  In order to query the mlflow database from your code, you need a package able to connect to a _Postgres_ database. Let's use the _psycopg_ package that we have installed earlier.

  Here is how you can query the database:

  ``` bash
  import psycopg2
  import psycopg2.extras

  tracking_db_uri = os.environ.get("MLFLOW_TRACKING_DB")

  conn = psycopg2.connect(tracking_db_uri)

  cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

  mlflow_query = """
  SELECT * FROM experiments;
  """

  cur.execute(mlflow_query)

  results = cur.fetchall()
  ```
</details>

## Simulate the passing of time

Where do we go from there ?

We have plugged into our workflow lifecycle the code to retrieve from the mlflow database the latest line on which the model has trained.

Let's play with the data engineer commands and see how the performance of our model behaves when we inject new data into the data source.

❓ **How do you inject new data in the data source ?**

The data engineer provided two sets of commands...

If you configured your `.env` so that your code sources the data from your local disk:
- `make reset_data_sources` will remove temporary data from your `data` directory
- `make show_data_sources` will show the data available for injection in your data source
- `make get_new_month` will inject one month worth of new data in your data source

If your code sources the data from Big Query:
- `make reset_bq_tables` will reset the Big Query dataset specified in your `.env`
- `make show_bq_tables` will show the state of your Big Query dataset tables
- `make push_month_to_bq` will inject one month worth of new data in your Big Query dataset table

Use either of those however you prefer.

... And remember that you can still use:
- `make list` to list all the available commands (including those new ones)
- `make show_env` to have a glance at the configuration of your project

Now your goal will be to alternate for example `make get_new_month` and `make run_flow` to inject new data and run a whole workflow lifecycle.

**💻 Run the `make get_new_month` and `make run_flow` commands until there is no more data to process**

👀 Have a look at the evolution of the performance in **mlflow**

**🧪 Run the tests with `make dev_test`**

👉 `test_shifts_complete` should be ✅

🏁 Congrats! Your workflow lifecycle is ready to be shipped in production 🔥
