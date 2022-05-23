
from tests.test_base import TestBase

import re

import pandas as pd


class TestMlflow(TestBase):

    def test_mlflow_parameters(self):
        """
        verify that the mlflow parameters are correctly set
        """

        experiment = self.load_results("test_mlflow_experiment")
        model_name = self.load_results("test_mlflow_model_name")
        tracking_uri = self.load_results("test_mlflow_tracking_uri")

        experiment_match = re.compile("^taxifare_experiment_.*$").match(experiment)
        model_name_match = re.compile("^taxifare_.*$").match(model_name)

        assert tracking_uri == "https://mlflow.lewagon.ai" or tracking_uri == "https://mlflow.lewagon.ai/"

        assert experiment_match is not None
        assert model_name_match is not None

    def test_mlflow_push_params(self):
        """
        verify params loaded in mlflow for experiment
        """

        params_df = pd.read_csv(_get_location("test_mlflow_push_params.csv.txt"))

        learning_rate_df = params_df[params_df.param_key == "learning_rate"]
        batch_size_df = params_df[params_df.param_key == "batch_size"]
        context_df = params_df[params_df.param_key == "context"]

        assert len(learning_rate_df) != 0 or len(batch_size_df) != 0 or len(context_df) != 0

    def test_mlflow_push_metrics(self):
        """
        verify metrics loaded in mlflow for experiment
        """

        metrics_df = pd.read_csv(_get_location("test_mlflow_push_metrics.csv.txt"))

        val_mae_df = metrics_df[metrics_df.metric_key == "val_mae"]
        mean_val_df = metrics_df[metrics_df.metric_key == "mean_val"]
        mae_df = metrics_df[metrics_df.metric_key == "mae"]

        assert len(val_mae_df) != 0 or len(mean_val_df) != 0 or len(mae_df) != 0

    def test_mlflow_push_model(self):
        """
        verify model loaded in mlflow for experiment
        """

        model_df = pd.read_csv(_get_location("test_mlflow_push_model.csv.txt"))

        assert len(model_df) != 0

    def test_mlflow_pred_model(self):

        pred_df = pd.read_csv(_get_location("test_mlflow_pred_model.csv.txt"))

        assert len(pred_df) != 0


def _query_mlflow_db(query):
    """
    query db
    """

    import psycopg2
    import psycopg2.extras

    tracking_db_uri = "postgresql://wagon_mlflo_1768:unSM_MPY4rA4t3b39fBL@wagon-mlflo-1768.postgresql.a.osc-fr1.scalingo-dbs.com:37750/wagon_mlflo_1768?sslmode=prefer"

    conn = psycopg2.connect(tracking_db_uri)

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query)

    results = cur.fetchall()

    return results


def _get_location(filename):
    """
    return test file location
    """

    import os

    return os.path.join(os.path.dirname(__file__), filename)


def _write_csv(results, filename):
    """
    write db results to csv
    """

    import csv

    params = [{k: v for k, v in line.items()} for line in results]

    with open(_get_location(filename), "w") as file:
        writer = csv.DictWriter(file, params[0].keys(), lineterminator="\n")
        writer.writeheader()
        for line in params:
            writer.writerow(line)


def write_mlflow_push_params(experiment):
    """
    retrieve pushed experiment params
    """

    query_params = f"""
        SELECT
            pa.key AS param_key,
            pa.value AS param_value
        FROM experiments ex
        JOIN runs ru ON ru.experiment_id = ex.experiment_id
        JOIN params pa ON pa.run_uuid = ru.run_uuid
        WHERE ex.name = '{experiment}';
    """

    results = _query_mlflow_db(query_params)

    _write_csv(results, "test_mlflow_push_params.csv.txt")  # do not ignore me


def write_mlflow_push_metrics(experiment):
    """
    retrieve pushed experiment metrics
    """

    query_metrics = f"""
        SELECT
            me.key AS metric_key,
            me.value AS metric_value
        FROM experiments ex
        JOIN runs ru ON ru.experiment_id = ex.experiment_id
        JOIN metrics me ON me.run_uuid = ru.run_uuid
        WHERE ex.name = '{experiment}';
    """

    results = _query_mlflow_db(query_metrics)

    _write_csv(results, "test_mlflow_push_metrics.csv.txt")


def write_mlflow_push_model(model_name):
    """
    retrieve pushed experiment metrics
    """

    query_metrics = f"""
        SELECT
            *
        FROM model_versions mv
        WHERE mv.name = '{model_name}'
        AND mv.current_stage = 'Production';
    """

    results = _query_mlflow_db(query_metrics)

    _write_csv(results, "test_mlflow_push_model.csv.txt")


def write_mlflow_pred_model():
    """
    make prediction with latest production model
    """

    from taxifare_model.interface.main import pred

    import os

    import pandas as pd

    # assert prediction is done through mlflow
    if os.environ.get("MODEL_TARGET") != "mlflow":

        raise NameError("prediction must be done through mlflow model")

    y_pred = pred()

    pred_df = pd.DataFrame(y_pred, columns=["prediction"])

    pred_df.to_csv(_get_location("test_mlflow_pred_model.csv.txt"))
