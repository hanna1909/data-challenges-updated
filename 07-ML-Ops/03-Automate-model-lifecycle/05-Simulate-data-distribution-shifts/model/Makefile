
#default: pytest
default: test_api_root test_api_predict

pytest:
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes

test_train_at_scale:
	TEST_ENV=development PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes

dev_test:
	@make write_results
	TEST_ENV=development PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes

# °º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸

# conf

TRAINING_PREFIX=train_${DATASET_SIZE}
TRAINING_PROCESSED_PREFIX=train_processed_${DATASET_SIZE}
VALIDATION_PREFIX=val_${DATASET_SIZE}

DATA_DIR=data
RAW_DIR=raw
TMP_DIR=tmp

fbold=$(shell echo "\033[1m")
fnormal=$(shell echo "\033[0m")

ccgreen=$(shell echo "\033[0;32m")
ccblue=$(shell echo "\033[0;34m")
ccreset=$(shell echo "\033[0;39m")

run_model:
	python -m taxifare_model.interface.main

# °º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸

# Prefect: run your workflow locally
run_flow:
	PREFECT__LOGGING__LEVEL=${PREFECT_LOG_LEVEL} python -m taxifare_flow.main

# °º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸

# Data sources: targets for monthly data imports

source_raw_train_url=https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_10k.csv
source_raw_monthly_source_url=https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_10k.csv

chunk_size_1=`expr ${CHUNK_SIZE} + 1`
chunk_size_p_1="+`expr ${CHUNK_SIZE} + 1`"
chunk_size_p_2="+`expr ${CHUNK_SIZE} + 2`"

data_tmp_source=${DATA_DIR}/${TMP_DIR}/monthly_data_source.csv
data_tmp_header=${DATA_DIR}/${TMP_DIR}/header.csv
data_tmp_diff=${DATA_DIR}/${TMP_DIR}/monthly_data_diff.csv
data_tmp_diff_head=${DATA_DIR}/${TMP_DIR}/monthly_data_diff_header.csv

data_raw_train=${DATA_DIR}/${RAW_DIR}/${TRAINING_PREFIX}.csv

bq_training_table=${DATASET}.${TRAINING_PREFIX}

show_data_sources:
	@echo "\n$(ccgreen)data sources:$(ccreset)"
	@ls -la ${data_tmp_source} ${data_tmp_header} ${data_tmp_diff} ${data_tmp_diff_head} ${data_raw_train}

	@echo "\n$(ccblue)data source line count:$(ccreset)"
	@wc -l ${data_tmp_source}
	@wc -l ${data_tmp_header}
	@wc -l ${data_tmp_diff}
	@wc -l ${data_tmp_diff_head}
	@wc -l ${data_raw_train}

show_bq_tables:
	@echo "\n$(ccblue)big query tables:$(ccreset)"
	@bq query --nouse_legacy_sql "SELECT * FROM ${DATASET}.INFORMATION_SCHEMA.PARTITIONS"

reset_data_sources:
	@mkdir -p ${DATA_DIR}/${TMP_DIR}/
	@echo "\n$(ccgreen)reset ${data_tmp_source}$(ccreset)"
	@curl ${source_raw_monthly_source_url} > ${data_tmp_source}
	@echo "\n$(ccgreen)reset ${data_tmp_header}$(ccreset)"
	@head -n 1 ${data_tmp_source} > ${data_tmp_header}
	@echo "\n$(ccgreen)reset ${data_tmp_diff}$(ccreset)"
	@echo "\c" > ${data_tmp_diff}
	@echo "\n$(ccgreen)reset ${data_tmp_diff_head}$(ccreset)"
	@head -n 1 ${data_tmp_header} > ${data_tmp_diff_head}
	@echo "\n$(ccgreen)reset ${data_raw_train}$(ccreset)"
	@curl ${source_raw_train_url} > ${data_raw_train}
	@make show_data_sources

reset_bq_tables:
	@echo "\n$(ccgreen)reset big query ${bq_training_table}$(ccreset)"
	@curl ${source_raw_train_url} > tmp_data.csv
	@bq load --autodetect --replace ${bq_training_table} tmp_data.csv
	@make show_bq_tables

get_new_month:
	@echo "\n$(ccgreen)import ${CHUNK_SIZE} lines from ${data_tmp_source} to ${data_tmp_diff}$(ccreset)"
	@$(shell zsh -c "diff <(head -n 1 ${data_tmp_source}) <(head -n 1 ${data_tmp_header}) > tmp_diff.csv")
	@if [[ -s tmp_diff.csv ]]; then \
		echo "there is a difference in the headers, this is a middle batch"; \
		head -n ${CHUNK_SIZE} ${data_tmp_source} > ${data_tmp_diff}; \
		tail -n ${chunk_size_p_1} ${data_tmp_source} > tmp_data.csv && mv tmp_data.csv ${data_tmp_source}; \
	else \
		echo "the headers are the same, this is the first batch"; \
		head -n ${chunk_size_1} ${data_tmp_source} | tail -n ${CHUNK_SIZE} > ${data_tmp_diff}; \
		tail -n ${chunk_size_p_2} ${data_tmp_source} > tmp_data.csv && mv tmp_data.csv ${data_tmp_source}; \
	fi
	@head -n 1 ${data_tmp_header} > ${data_tmp_diff_head}
	@cat ${data_tmp_diff} >> ${data_tmp_diff_head}
	@echo "\n$(ccgreen)import all lines from ${data_tmp_diff} to ${data_raw_train}$(ccreset)"
	@cat ${data_tmp_diff} >> ${data_raw_train}
	@make show_data_sources

push_month_to_bq:
	@if [[ -s ${data_tmp_diff} ]]; then \
		echo "\n$(ccgreen)push ${data_tmp_diff_head} to big query ${bq_training_table}$(ccreset)"; \
		bq load --autodetect --noreplace ${bq_training_table} ${data_tmp_diff_head}; \
	else \
		echo "\n$(ccgreen)no more data to push to big query ${bq_training_table}$(ccreset)"; \
	fi
	@make show_bq_tables

show_env:
	@echo "\nEnvironment variables used by the \`taxifare-model\` package loaded by \`direnv\` from your \`.env\` located at:"
	@echo ${DIRENV_DIR}

	@echo "\n$(ccgreen)local storage:$(ccreset)"
	@env | grep -E "LOCAL_DATA_PATH|LOCAL_REGISTRY_PATH" || :
	@echo "\n$(ccgreen)dataset:$(ccreset)"
	@env | grep -E "DATASET_SIZE|VALIDATION_DATASET_SIZE|CHUNK_SIZE" || :
	@echo "\n$(ccgreen)package behavior:$(ccreset)"
	@env | grep -E "DATA_SOURCE|MODEL_TARGET" || :

	@echo "\n$(ccgreen)GCP:$(ccreset)"
	@env | grep -E "PROJECT|REGION" || :
	@echo "\n$(ccgreen)Cloud Storage:$(ccreset)"
	@env | grep -E "BUCKET_NAME|BLOB_LOCATION" || :

	@echo "\n$(ccgreen)Big Query:$(ccreset)"
	@env | grep -E "DATASET" | grep -Ev "DATASET_SIZE|VALIDATION_DATASET_SIZE" || :

	@echo "\n$(ccgreen)Compute Engine:$(ccreset)"
	@env | grep -E "INSTANCE" || :

	@echo "\n$(ccgreen)MLflow:$(ccreset)"
	@env | grep -E "MLFLOW_EXPERIMENT|MLFLOW_MODEL_NAME" || :
	@env | grep -E "MLFLOW_TRACKING_URI|MLFLOW_TRACKING_DB" || :

	@echo "\n$(ccgreen)Prefect:$(ccreset)"
	@env | grep -E "PREFECT_BACKEND|PREFECT_FLOW_NAME|PREFECT_LOG_LEVEL" || :

reinstall_package:
	@pip uninstall -y taxifare-model || :
	@pip install -e .

write_results:

	@echo "verify installed packages versions"
	@pip show taxifare-model | grep 'Summary' > tests/all/test_package_version.txt || :

	@echo "${MLFLOW_DB_USER}" > tests/shifts/test_shifts_db_user.txt
	@echo "${MLFLOW_DB_PASSWORD}" > tests/shifts/test_shifts_db_password.txt
	@echo "${MLFLOW_DB_HOSTNAME}" > tests/shifts/test_shifts_db_hostname.txt
	@echo "${MLFLOW_DB_PORT}" > tests/shifts/test_shifts_db_port.txt
	@echo "${MLFLOW_DB_NAME}" > tests/shifts/test_shifts_db_name.txt
	@echo "${MLFLOW_TRACKING_DB}" > tests/shifts/test_shifts_tracking_db.txt

list:
	@echo "\nHelp for the \`taxifare-model\` package \`Makefile\`"

	@echo "\n$(ccgreen)$(fbold)PACKAGE$(ccreset)"

	@echo "\n    $(ccgreen)$(fbold)environment rules:$(ccreset)"
	@echo "\n        $(fbold)show_env$(ccreset)"
	@echo "            Show the environment variables used by the package by category."

	@echo "\n    $(ccgreen)$(fbold)run rules:$(ccreset)"
	@echo "\n        $(fbold)run_model$(ccreset)"
	@echo "            Run the package (\`taxifare_model.interface.main\` module)."

	@echo "\n        $(fbold)run_flow$(ccreset)"
	@echo "            Start a prefect workflow locally (run the \`taxifare_flow.main\` module)."

	@echo "\n$(ccgreen)$(fbold)WORKFLOW$(ccreset)"

	@echo "\n    $(ccgreen)$(fbold)data operation rules:$(ccreset)"
	@echo "\n        $(fbold)show_data_sources$(ccreset)"
	@echo "            Show the local data sources."
	@echo "\n        $(fbold)show_bq_tables$(ccreset)"
	@echo "            Show the Big Query dataset tables used by the package."
	@echo "\n        $(fbold)reset_data_sources$(ccreset)"
	@echo "            Reset the content of the local CSV files."
	@echo "\n        $(fbold)reset_bq_tables$(ccreset)"
	@echo "            Reset the content of the Big Query dataset tables used by the package."
	@echo "\n        $(fbold)get_new_month$(ccreset)"
	@echo "            Get one more month in the local dataset to simulate the passing of time."
	@echo "\n        $(fbold)push_month_to_bq$(ccreset)"
	@echo "            Get one more month in the Big Query dataset to simulate the passing of time."

	@echo "\n$(ccgreen)$(fbold)TESTS$(ccreset)"

	@echo "\n    $(ccgreen)$(fbold)student rules:$(ccreset)"
	@echo "\n        $(fbold)reinstall_package$(ccreset)"
	@echo "            Install the version of the package corresponding to the challenge."
	@echo "\n        $(fbold)dev_test$(ccreset)"
	@echo "            Run the tests."

	@echo "\n    $(ccblue)$(fbold)internal rules:$(ccreset)"
	@echo "\n        $(fbold)write_results$(ccreset)"
	@echo "            Write the test results so they can be added and committed to git."
	@echo "\n        $(fbold)pylint$(ccreset)"
	@echo "            Print a report on code style."
	@echo "\n        $(fbold)pytest$(ccreset)"
	@echo "            Run the tests and print a test report."

