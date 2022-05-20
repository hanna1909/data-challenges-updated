
# How does this package work

## `taxifare_model` package

- `interface/main.py` contains all the routes needed for the V1 of the package, which can train on a limited number of rows
- `interface/main_incremental.py` contains all the routes needed for the V2 of the package, which can train incrementally on an unlimited number of rows!
- `ml_logic/params.py` are global project params to set up manually

``` bash
python -m taxifare_model.interface.main
```

[//]: # ( $ONLY_FROM_prefect_BEGIN )
## `taxifare_flow` package

- `main.py` runs a complete model lifecycle, either locally or through a prefect backend
- `flow.py` creates a graph of the tasks of the model lifecycle and runs it for a test iteration of 7 days

``` bash
python -m taxifare_flow.main
```
[//]: # ( $ONLY_FROM_prefect_END )
