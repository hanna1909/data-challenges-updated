import os
from taxifare.flow.flow import build_flow
flow = build_flow()

mlflow_experiment = os.environ.get("MLFLOW_EXPERIMENT")
prefect_backend = os.environ.get("PREFECT_BACKEND")

# YOUR CODE HERE

if prefect_backend == "development":
    # `make run_workflow`` will run all tasks directly on your terminal (you can see your logs in your terminal)
    flow.visualize()
    flow.run(parameters=dict(experiment=mlflow_experiment))

elif prefect_backend == "production":
    # `make run_workflow` only send a "snapshot" of your python code to Prefect (but does not executes it). Use it when you change your python code
    from dotenv import dotenv_values
    env_dict = dotenv_values(".env")
    flow.run_config = LocalRun(env=env_dict)
    flow.register("taxifare_project")
else:
    raise ValueError(f"{prefect_backend} is not a valid value for PREFECT_BACKEND")
