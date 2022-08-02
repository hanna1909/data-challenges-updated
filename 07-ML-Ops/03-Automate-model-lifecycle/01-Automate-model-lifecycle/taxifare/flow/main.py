# YOUR CODE HERE

flow = build_flow()

mlflow_experiment = os.environ.get("MLFLOW_EXPERIMENT")
prefect_backend = os.environ.get("PREFECT_BACKEND")

if prefect_backend == "development":
    flow.visualize()
    flow.run(parameters=dict(
        experiment=mlflow_experiment))
elif prefect_backend == "production":
    flow.register("taxifare_project")
else:
    raise ValueError(f"{prefect_backend} is not a valid value for PREFECT_BACKEND")
