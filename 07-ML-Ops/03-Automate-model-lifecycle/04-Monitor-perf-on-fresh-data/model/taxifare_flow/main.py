
# YOUR CODE HERE


flow = build_flow()

flow.visualize()

mlflow_experiment = os.environ.get("MLFLOW_EXPERIMENT")

if os.environ.get("PREFECT_BACKEND") == "local":

    flow.run(parameters=dict(
        experiment=mlflow_experiment))

else:

    # requires cli run:
    # `prefect create project "taxifare_project"`

    flow.register("taxifare_project")
