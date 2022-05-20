# ⛰ "Train At Scale" Unit 🗻

In this unit, you will learn how to package the notebook provided by the Data Science team at WagonCab, and how to scale it so that it can be trained on the full dataset locally on your machine.

This unit consist of the 5 challenges below, that are all regrouped in this single readme file. Simply follow the guide, step by step!

1. **LOCAL SETUP**: Structure the code into an installable python package, make sure your VS code is setup for the week and be ready to say goodbye to jupyter notebooks!
2. **UNDERSTAND DATA SCIENTIST WORK**: Discover the notebook provided by the Data Science team
3. **FROM NOTEBOOK TO PACKAGE**: Discover the notebook provided by the Data Science team
4. **INVESTIGATE BOTTLENECKS**: Now that we have an operable package, we will discover how to explore and correct the slower parts of our code
5. **INCREMENTAL PROCESSING**: We will see how to preprocess the dataset incrementally so that we can process a volume of data that does not fit into memory
6. **INCREMENTAL LEARNING**
Finally we will see how to train the model without ever loading all data at once in memory.


# 1️⃣ LOCAL SETUP

<details>
  <summary markdown='span'><strong>❓ instructions (expand me)</strong></summary>

<br>

As lead ML Engineer for the project, your first role is to setup a local working environment (pyenv) and a python package that only contains the skeleton of your code base.

💡 Packaging notebooks is a key ML Engineer skill. It allows
- Other users to collaborate on the code
- To call the code locally or on a remote machine in order for example to train the `taxifare_model` on a bigger machine
- To put the code in production (on a server that never stops running) in order to expose it as an **API** or through a **website**
- Render the code operable so that it can be ran manually or plugged to an automation workflow

### 1.1) Create new pyenv [🐍 taxifare-model]

```bash
cd ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-OPS/01-Train-at-scale/01-Train-at-scale/model
python --version # First, check your <YOUR_PYTHON_VERSION>. For example: 3.8.12
```

```
pyenv virtualenv <YOUR_PYTHON_VERSION> taxifare-model
pip install --upgrade pip
pyenv local taxifare-model
code .
```

Then, make sure both your OS terminal, your VS-code integrated terminal display well [🐍 taxifare-model] when in `model` folder.
On VS code, open any python file and check that taxifare-model is also activated by clicking on the bottom right pyenv section as below
<img src='https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/pyenv-setup.png'>

### 1.2) Get familiar with the model package boilerplate

👇 Take 15 min to understand the boilerplate we've prepared for you

```bash
. # ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-OPS/01-Train-at-scale/01-Train-at-scale/model
├── Makefile          # Main "interface" with your project. Use to launch tests, or start trainings etc... from the CLI
├── README.md         # A readme that explains the project to your teammates
├── data              # empty folder that will be gitignored
│   ├── processed     # You will store intermediate processed data here as need be
│   └── raw           # You will download samples of the raw data from the internet to work/prototype locally
├── notebooks
│   ├── datascientist_deliverable.ipynb # The deliverable from the DS team!
│   └── recap.ipynb
├── pytest.ini        # test configuration file (do not touch)
├── requirements.txt  # list all third party packages to add to your local environment
├── setup.py          # allow to `pip install` your package
├── taxifare_model          # the code logic for this package
│   ├── __init__.py
│   ├── interface
│   │   ├── __init__.py
│   │   └── main_local.py   # Your main python entry point that contains all the "routes" that will be accessible from outside.
│   └── ml_logic
│       ├── __init__.py
│       ├── data.py         # save, load and clean data
│       ├── encoders.py     # custom encoders utilities
│       ├── model.py        # tensorflow model
│       ├── params.py       # global project params
│       ├── preprocessor.py # sklearn preprocessing pipelines
│       ├── registry.py     # save and load models
│       └── utils.py        # useful python functions
├── tests  # Tests to run using make pytest
    ├── ...
    ├── ...
└── training_outputs # local storage for trained model
    ├── metrics
    └── models
    └── params
```

👉 Let's install your package on this new virtual env.

```bash
cd ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-OPS/01-Train-at-scale/01-Train-at-scale/model
pip install -e .
```

Make sure the package is installed by running `pip list | grep taxifare_model`. It should print the absolute path to the package.


### 1.3) Download raw data locally on your drive

```bash
cd ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-OPS/01-Train-at-scale/01-Train-at-scale/model
# 3 train sets
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_1k.csv > data/raw/train_1k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_10k.csv > data/raw/train_10k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_100k.csv > data/raw/train_100k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_500k.csv > data/raw/train_500k.csv

# 3 val sets
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/val_1k.csv > data/raw/val_1k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/val_10k.csv > data/raw/val_10k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/val_100k.csv > data/raw/val_100k.csv
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/val_500k.csv > data/raw/val_500k.csv
```

❗️ And only if you have excellent internet connexion and 6Go free space on your computer (it's not mandatory for the week)
```bash
curl https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_50M.csv.zip > model/data/raw/train_50M.csv.zip
```
</details>

<br>


# 2️⃣ UNDERSTAND DATA SCIENTIST WORK

<details>
  <summary markdown='span'><strong>❓ instructions (expand me)</strong></summary>

<br>

Open `datascientist_deliverable.ipynb` within VScode (forget about Jupyter for this module)

❗️ Make sure to use `taxifare_model` as ipykernel venv

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/pyenv-notebook.png'>

- Run all cells carefully while understanding them. This handover between you and the DS team is the perfect time to interact with them.
- If some packages are missing, add them to your `requirements.txt` and `pip install -e .` again

</details>

<br>


# 3️⃣ PACKAGE CODE

<details>
  <summary markdown='span'><strong>❓ instructions (expand me)</strong></summary>

<br>

🎯 Your goal is to be able to run the `taxifare_model.interface.main_local` module as per below

```bash
# -> model
python -m taxifare_model.interface.main_local
```

To do so, please code the missing code marked `# YOUR CODE HERE` in the following files

```markdown
├── taxifare_model
│   ├── __init__.py
│   ├── interface
│   │   ├── __init__.py
│   │   └── main_local.py   # ❓ Start by here: code `preprocess_and_train`, `pred`
│   └── ml_logic
│       ├── __init__.py
│       ├── data.py         # ❓ `clean data`
│       ├── encoders.py     # ❓ `transform_time_features`, `transform_lonlat_features`, `compute_geohash`
│       ├── model.py        # ❓ `initialize_model`, `compile_model`, `train_model`
│       ├── params.py       # ✅ You can change `DATASET_SIZE`
│       ├── preprocessor.py # ❓ `preprocess_features`
│       ├── registry.py     # ✅ `save_model` and `load_model` are already coded for you
│       └── utils.py        # ✅ keep for later
```

We have written various tests to help you check your code step-by-steps

```bash
# -> model
make test_train_at_scale
```

👉 To mimic Data Scientist setup, please check your logic at least once with the following DATASET_SIZE

```python
# taxifare_model/ml_logic/params.py
DATASET_SIZE = '100k'
```

But feel free to keep `'1k'` or `'10k'` datasets to iterate faster in debug mode 🐞 !


💡 Tips: Did you know you could convert `.ipynb` files into a single `.py` files with VScode? To do so, open any notebook, and use the command palette to select "Convert to Python Script". It may help you copy paste multiple cell logic at once.

</details>

<br>

# 4️⃣ INVESTIGATE SCALABILITY


<details>
  <summary markdown='span'><strong>❓ instructions (expand me)</strong></summary>

<br>

Now that you managed to make the package work for a small dataset, time to see how it will handle the real dataset!

👉 Switch `ml_logic.params.DATASET_SIZE` and `ml_logic.params.VALIDATION_DATASET_SIZE` to `'500k'` to start getting serious!

❓ Investigate **which part of your code takes the most time and memory usage** and try to answer the following questions with your buddy:
- [ ] What part of your code holds the key bottlenecks?
- [ ] What kind of bottlenecks are the most worrying? (Time, Memory?)
- [ ] Do you think it will scale to 50M rows?
- [ ] Can you think about potential solutions? Write down your ideas, but do not implement them yet!

💡 Hint: Use `ml_logic.utils.simple_time_and_memory_tracker` to decorate the methods of your choice as below

```python
# taxifare_model.ml_logic.data.py
from taxifare_model.ml_logic.utils import simple_time_and_memory_tracker

@simple_time_and_memory_tracker
def clear_data() -> pd.DataFrame:
    ...
```
And make sure to understand exactly how decorators work. Refer to lecture [0405-Communicate](https://kitt.lewagon.com/camps/<user.batch_slug>/lectures/content/04-Decision-Science_05-Communicate.slides.html?title=Communicate#/6/3)


</details>

<br>


# 5️⃣ INCREMENTAL PROCESSING

<details>
  <summary markdown='span'><strong>❓ instructions (expand me)</strong></summary>

<br>

🎯 Your goal is to improve your codebase so as **to be able to process our model on `50M` rows or even more, without RAM limits**.

### 5.1) Discussion

**What did we learn?**
From previous challenge, we've seen that we have memory and time constraints:
- the `(55M,8)` `raw_data` loaded in memory as dataframe takes about 12GB of RAM, which is too much for most computers.
- the `(55M,65)` preprocessed dataframe is even bigger.
- the `ml_logic.encoders.compute_geohash` method takes an awful long time to process 🤯

**What could we do?**

1. One solution is to buy **more RAM from a Virtual Machine** in the cloud and process it there (and it is often the simplest way to deal with such problem)
2. Another could be to load each column of the `raw_data` individually, and prepare some preprocessing on it, **column by column**
```python
for col in column_names:
    df_col = pd.read_csv("raw_data.csv.zip", usecols=col)
    # do preprocessing on the single column here
```
3. But you may always encounter datasets "too big to load anyway"! By the way, the [real NYC dataset](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) is even bigger than 55M rows and actually weight about 156GB !

**Proposed solution: incremental preprocessing 🔪 chunk-by-chunk 🔪**

Did you notice our preprocessing is **stateless**?
- We don't need to store (fit) any information on the train set such as _standard deviation_ for each columns, to apply it (transform) on the test set.
- We can therefore decouple/split the preprocessing from the training instead of grouping everything into a pipeline `preprocess_and_train`. We will `preprocess` and store `data_processed` once-for-all on our hard drive, then `train` our model from that `data_processed` later on. When new data will arrive, we'll simply apply the preprocessing to it as a pure python function.

Secondly, as we do not need to compute _column-wise-statistics_ but only perform _row-by-row preprocessing_, we can do the preprocessing **chunk by chunk**, with chunks of limited size (e.g 100_000 rows), each chunk fitting nicely in memory! And then simply append each _processed chunk_ at the end of a CSV on our local disk. It won't make it faster but at least it will compute without crashing. And you only need to do it once.

```python
data_chunk = pd.read_csv(
        data_raw_path,
        skiprows=...
        nrows=...
        )
```

### 5.2) Your turn ❓

❓ First, bring back smaller dataset sizes while you try to make it work.
```
# params.py
DATASET_SIZE = '1k'
VALIDATION_DATASET_SIZE = '1k'
CHUNK_SIZE = 200
```

**❓ Then, copy paste and try to code this new route in your `ml_logic.interface.main_local` module**

[//] TODO: 🚨 Code below is not the single source of truth. Find a way to remove this dual-source! 🚨
```python
def preprocess(training_set=True):
    """
    Preprocess the dataset iteratively, loading data by chunks fitting in memory,
    processing each chunk, appending each of them to a final dataset preprocessed,
    and saving final prepocessed dataset as CSV
    """

    print("\n⭐️ use case: preprocess")

    # local saving paths given to you (do not overwrite these data_path variable)
    if training_set:
        source_name = f"train_{DATASET_SIZE}.csv"
        destination_name = f"train_processed_{DATASET_SIZE}.csv"
    else:
        source_name = f"val_{VALIDATION_DATASET_SIZE}.csv"
        destination_name = f"val_processed_{VALIDATION_DATASET_SIZE}.csv"

    data_raw_path = os.path.abspath(os.path.join(
        ROOT_PATH, "data", "raw", source_name))
    data_processed_path = os.path.abspath(os.path.join(
        ROOT_PATH, "data", "processed", destination_name))

    # iterate on the dataset, by chunks
    chunk_id = 0

    while (True):
        print(f"processing chunk n°{chunk_id}...")

        # load in memory the chunk numbered `chunk_id` of size CHUNK_SIZE
        # 🎯 Hint: check out pd.read_csv(skiprows=..., nrows=...)

        # YOUR CODE HERE

        # clean chunk
        # YOUR CODE HERE

        # create X_chunk,y_chunk
        # YOUR CODE HERE

        # create X_processed_chunk and concatenate (X_processed_chunk, y_chunk) into data_processed_chunk
        # YOUR CODE HERE

        # Save the chunk of the dataset to local disk (append to existing csv to build it chunk by chunk)
        # 🎯 Hints1: check out pd.to_csv(mode=...)
        # YOUR CODE HERE

        chunk_id += 1

    # 🧪 Write tests. Check your results with `make test_train_at_scale`
    data_processed = pd.read_csv(data_processed_path, header=None, dtype=DATA_PROCESSED_DTYPES_OPTIMIZED).to_numpy()
    write_result(name="test_preprocess", subdir="train_at_scale",
                 data_processed_head=data_processed[0:2])

    print("✅ data processed saved entirely")
```

**🧪 Test your code**
When you are happy with your results, test your code with `make test_train_at_scale`

**❓ Create and store the 4 large preprocessed datasets**
- `data/processed/train_processed_500k.csv`
- `data/processed/val_processed_500k.csv`

By changing `params.py` as below 👇

```python
# params.py
DATASET_SIZE = '500k'
VALIDATION_DATASET_SIZE = '500k'
CHUNK_SIZE = 100000
```

</details>

<br>


# 6️⃣ INCREMENTAL LEARNING


<details>
  <summary markdown='span'><strong>❓ instructions (expand me)</strong></summary>

<br>

🎯 Goal: Train our model on the full `data_processed.csv`

### 6.1) Discussion

We cannot load such dataset in RAM all at once, but we can load it chunk by chunk.

How do we train a model "chunk by chunk" ?

This is called **incremental learning** or **partial_fit**
- We initialize a model with random weights ${\theta_0}$
- We load the first `data_processed_chunk` in memory (say, 100_000 rows)
- We train model on the first chunk , and update its weights accordingly ${\theta_0} \rightarrow {\theta_1}$
- We load the second `data_processed_chunk` in memory
- We *retrain* model with this second chunk, this time updating previously computed weights ${\theta_1} \rightarrow {\theta_2}$!
- etc... until the end of the entire dataset

<br>

❗️ Not all machine-learning model support incremental learning: only *parametric* models $f_{\theta}$ that are based on *iterative update methods* like gradient descent do
- In **scikit-learn**, `model.partial_fit()` is only available SGDRegressor/Classifier and few others ([read this carefully 📚](https://scikit-learn.org/0.15/modules/scaling_strategies.html#incremental-learning)).
- In **tensorflow** and another other deep learning framework, training is always iterative and incremental learning is the default behavior! You just need to avoid calling `model.initialize()` between two chunks!

<br>

❗️ Do not confuse `chunk_size` with `batch_size` from deep learning
- For each chunk (big), your model will read data batch-per-batch (small) many times over (epochs)

<br>

👍 **Pros:**: This universal approach is framework independent. You can use it with scikit-learn, XGBoost, Tensorflow etc...

<details>
  <summary markdown='span'><strong>Do we really need chunks with tensorflow?</strong></summary>

Granted, thanks to tensorflow `Datasets` you will not always need "chunks" as you can use batch-per-batch dataset loading as below (we will see it in recap)

```python
import tensorflow as tf
ds = tf.data.experimental.make_csv_dataset(data_processed_55M.csv, batch_size=256)
model.fit(ds)
```

However, we would like to teach you the universal method of incremental fit by chunk in this challenge, as it applies to any framework, and will prove useful to *partially retrain* your model with newer data once it is put in production.
</details>

<br>

👎 **Cons**: The model will be biased towards fitting the *latest chunk* better than the *first* ones. In our case, it is not a problem as our training dataset is shuffled, but it is important to keep that in mind when we will do a partial-fit of our model with newer data once it is in production.


### 6.2) Your turn ❓

**❓ Copy paste and try to code this new route in your `ml_logic.interface.main_local` module**

[//] TODO: 🚨find a way to remove this dual-source-of-truth! 🚨

```python
def train():
    """
    Training on the full (already preprocessed) dataset, by loading it
    chunk-by-chunk, and updating the weight of the model for each chunks.
    Save model, compute validation metrics on a holdout validation set that is
    common to all chunks.
    """
    print("\n ⭐️ use case: train")

    # Validation Set: Load a validation set common to all chunks and create X_val, y_val
    # YOUR CODE HERE

    # Iterate on the full training dataset chunk per chunks. Break out of the loop if you receive no data to train upon!
    model = None
    chunk_id = 0
    metrics_val_list = []  # store each metrics_val_chunk

    while (True):
        print(f"loading and training on preprocessed chunk n°{chunk_id}...")

        # Load chunk of preprocess data and create (X_train_chunk, y_train_chunk)
        # YOUR CODE HERE

        # Train a model incrementally
        learning_rate = 0.001
        batch_size = 256
        # YOUR CODE HERE

        chunk_id += 1

    params = dict(
        learning_rate=learning_rate,
        batch_size=batch_size,
        incremental=True,
        chunk_size=CHUNK_SIZE)

    # process metrics
    metrics_val_mean_all_chunks = None
    # YOUR CODE HERE
    metrics = dict(mean_val=metrics_val_mean_all_chunks)

    # Save model
    save_model(model, params=params, metrics=metrics)

    pass
```

**🧪 Test your code**
When you are happy with your results, test your code with `make test_train_at_scale`
Everything tests should be green 🏁

**Give it a try with the full dataset!**
```python
# params.py
DATASET_SIZE = '500k'
VALIDATION_DATASET_SIZE = '500k'
CHUNK_SIZE = 100000
```

Congratulations! 🏁

</details>

<br>
