# $DEL_ONLY_FROM_api_pred_BEGIN
FROM python:3.8.12-buster
COPY taxifare_model /taxifare_model
COPY taxifare_api /taxifare_api
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
CMD uvicorn taxifare_api.fast:app --host 0.0.0.0 --port $PORT
# $DEL_ONLY_FROM_api_pred_END
