# $DEL_BEGIN
FROM python:3.8.12-buster
COPY taxifare/interface /taxifare/interface
COPY taxifare/ml_logic /taxifare/ml_logic
COPY taxifare/api /taxifare/api
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
# $DEL_ONLY_FROM_api_pred_END
