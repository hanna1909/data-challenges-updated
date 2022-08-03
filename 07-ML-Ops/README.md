
[//]: # ( presentation of the module )

## Context: Welcome to the TaxiFare project team @ WagonCab 🚕

In this module, you will impersonate a **ML Engineer** at `WagonCab`, a new taxi-app startup opening in New York!

`WagonCab` is willing to launch a new ML-product in production called `TaxiFare`. It's goal is to integrate into its app the prediction of the price of conventional taxi rides in new york, in order to show its user how much money they would gain by comparison!

Your company has at its disposal the huge public [NYC Trip Record Dataset](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) which weights around 170 Go, and looks as follow

```markdown
|    | key                           |   fare_amount | pickup_datetime         |   pickup_longitude |   pickup_latitude |   dropoff_longitude |   dropoff_latitude |   passenger_count |
|---:|:------------------------------|--------------:|:------------------------|-------------------:|------------------:|--------------------:|-------------------:|------------------:|
|  0 | 2009-06-15 17:26:21.0000001   |           4.5 | 2009-06-15 17:26:21 UTC |           -73.8443 |           40.7213 |            -73.8416 |            40.7123 |                 1 |
|  1 | 2010-01-05 16:52:16.0000002   |          16.9 | 2010-01-05 16:52:16 UTC |           -74.016  |           40.7113 |            -73.9793 |            40.782  |                 1 |
|  2 | 2011-08-18 00:35:00.00000049  |           5.7 | 2011-08-18 00:35:00 UTC |           -73.9827 |           40.7613 |            -73.9912 |            40.7506 |                 2 |
|  3 | 2012-04-21 04:30:42.0000001   |           7.7 | 2012-04-21 04:30:42 UTC |           -73.9871 |           40.7331 |            -73.9916 |            40.7581 |                 1 |
|  4 | 2010-03-09 07:51:00.000000135 |           5.3 | 2010-03-09 07:51:00 UTC |           -73.9681 |           40.768  |            -73.9567 |            40.7838 |                 1 |
```

A team of **Data Scientists** has been staffed to create and fine-tune a machine learning model to predict the price of a ride.
They have been working in a isolated notebook context, hand-crafting & fine-tuning the best possible model, trained on a small, manageable subset of this dataset.

## Plan of the module (5 units)

**Unit 1) - Train at Scale**
- Understand data scientists' notebooks
- **Package** your python code
- Master your **IDE** (bye bye jupyter, hello VS code)
- Train at scale (locally) via **incremental** processing techniques

**Unit 2) - Train on Cloud**
- Master your own **shell**
- Store model weights on **Google Cloud Storage**
- Store & query data on **Google Big Query**
- Use cloud power with **Google Compute Engine** (Virtual Machines)
- Use cloud managed solution with **Google Wertex AI Workbench** (Jupyter Lab on the cloud)

**Unit 3) - Model Lifecycle**
- store model versions and monitor performance with **ML FLOW**
- Retrain on fresh new data using **Prefect** to manage your DAG (Direct Acyclic Graphs)
- Learn about **data versionning**

**Unit 4) - Predict in production**
- Develop your **API** with **FastAPI** and **uvicorn**
- Create a **Docker image** for your app
- Deploy Docker containers to production using **Google Cloud Run**

**Unit 5) - User interface**
- Develop a user interface with **Streamlit**
- **Plug** a user interface to your FastAPI
- **Deploy** your front end on **Streamlit Cloud** (or Cloud Run or Heroku)
