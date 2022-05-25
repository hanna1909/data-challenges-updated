
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

reinstall_package:
	@pip uninstall -y taxifare-model || :
	@pip install -e .

write_results:

	@echo "verify installed packages versions"
	@pip show taxifare-model | grep 'Summary' > tests/all/test_package_version.txt || :

	@echo "retrieve bucket content..."
	@gsutil stat "gs://${BUCKET_NAME}/data/train_10k.sample.csv" > tests/cloud_data/test_cloud_data_uploaded_blob.txt || :
	@gsutil stat "gs://${BUCKET_NAME}/data/val_10k.sample.csv" > tests/cloud_data/test_cloud_data_uploaded_blob_val.txt || :
	@echo "${DATASET}" > tests/cloud_data/test_cloud_data_create_dataset.txt
	@echo "retrieve biq query dataset list..."
	@$(shell sh -c "echo YnEgbHMK= | base64 -d") > tests/cloud_data/test_cloud_data_create_dataset_source.txt || :
	@echo "${TRAINING_PREFIX}" > tests/cloud_data/test_cloud_data_create_training_table.txt
	@echo "${VALIDATION_PREFIX}" > tests/cloud_data/test_cloud_data_create_validation_table.txt
	@echo "retrieve biq query dataset table list..."
	@$(shell sh -c "echo YnEgbHMK= | base64 -d") ${DATASET} > tests/cloud_data/test_cloud_data_create_table_source.txt || :
	@echo "retrieve biq query training table description..."
	@$(shell sh -c "echo YnEgc2hvdwo= | base64 -d") ${DATASET}.${TRAINING_PREFIX} > tests/cloud_data/test_cloud_data_table_content_training.txt || :
	@echo "retrieve biq query validation table description..."
	@$(shell sh -c "echo YnEgc2hvdwo= | base64 -d") ${DATASET}.${VALIDATION_PREFIX} > tests/cloud_data/test_cloud_data_table_content_validation.txt || :
	@echo "retrieve biq query training table first rows..."
	@bq query --use_legacy_sql=false "SELECT fare_amount FROM ${DATASET}.${TRAINING_PREFIX} LIMIT 10" > tests/cloud_data/test_cloud_data_bq_chunks.txt || :

list:
	@echo "\nHelp for the \`taxifare-model\` package \`Makefile\`"

	@echo "\n$(ccgreen)$(fbold)PACKAGE$(ccreset)"

	@echo "\n    $(ccgreen)$(fbold)environment rules:$(ccreset)"
	@echo "\n        $(fbold)show_env$(ccreset)"
	@echo "            Show the environment variables used by the package by category."

	@echo "\n    $(ccgreen)$(fbold)run rules:$(ccreset)"
	@echo "\n        $(fbold)run_model$(ccreset)"
	@echo "            Run the package (\`taxifare_model.interface.main\` module)."

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

