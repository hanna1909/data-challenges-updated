default:
	@echo 'tests are only executed locally for this challenge'

test_train_at_scale: test_train_at_scale_3 \
	test_train_at_scale_5 \
	test_train_at_scale_6

test_train_at_scale_3:
	@pytest \
	tests/train_at_scale/test_data.py \
	tests/train_at_scale/test_preprocessing.py \
	tests/train_at_scale/test_model.py \
	tests/train_at_scale/test_interface.py::TestInterface::test_preprocess_and_train_pass \
	tests/train_at_scale/test_interface.py::TestInterface::test_preprocess_and_train_value \
	tests/train_at_scale/test_interface.py::TestInterface::test_pred_pass \
	tests/train_at_scale/test_interface.py::TestInterface::test_pred_value

test_train_at_scale_5:
	@pytest \
	tests/train_at_scale/test_interface.py::TestInterface::test_preprocess_pass \
	tests/train_at_scale/test_interface.py::TestInterface::test_preprocess_value

test_train_at_scale_6:
	@pytest \
	tests/train_at_scale/test_interface.py::TestInterface::test_train_pass \
	tests/train_at_scale/test_interface.py::TestInterface::test_train_value

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
	python -m taxifare.interface.main

# $ONLY_FROM_setup_BEGIN
	@echo "\n$(ccgreen)GCP:$(ccreset)"
	@env | grep -E "PROJECT|REGION" || :
	@echo "\n$(ccgreen)Cloud Storage:$(ccreset)"
	@env | grep -E "BUCKET_NAME|BLOB_LOCATION" || :
# $ONLY_FROM_setup_END

# $ONLY_FROM_cloud_data_BEGIN
	@echo "\n$(ccgreen)Big Query:$(ccreset)"
	@env | grep -E "DATASET" | grep -Ev "DATASET_SIZE|VALIDATION_DATASET_SIZE" || :
# $ONLY_FROM_cloud_data_END

reinstall_package:
	@pip uninstall -y taxifare-model || :
	@pip install -e .

write_results:
	@python -m tests.notebook.write_train

# $ONLY_FOR_setup_BEGIN
	@echo "verify gcloud auth..."
	@gcloud auth list > tests/setup/test_setup_cli_auth.txt 2>&1 || :
	@echo "${PROJECT}" > tests/setup/test_setup_project_id.txt
	@echo "verify gcp default project..."
	@$(shell sh -c "echo Z2Nsb3VkIGNvbmZpZyBnZXQtdmFsdWUgcHJvamVjdAo= | base64 -d") > tests/setup/test_setup_env_project_id.txt || :
	@echo "${BUCKET_NAME}" > tests/setup/test_setup_bucket_name.txt
	@echo "verify bucket name..."
	@$(shell sh -c "echo Z3N1dGlsIGxzCg== | base64 -d") > tests/setup/test_setup_env_bucket_name.txt || :
# $ONLY_FOR_setup_END

# $ONLY_FOR_cloud_data_BEGIN
	@echo "retrieve bucket content..."
	@gsutil stat "gs://${BUCKET_NAME}/data/train_10k.sample.csv" > tests/cloud_data/test_cloud_data_uploaded_blob.txt || :
	@gsutil stat "gs://${BUCKET_NAME}/data/val_10k.sample.csv" > tests/cloud_data/test_cloud_data_uploaded_blob_val.txt || :
	@echo "${DATASET}" > tests/cloud_data/test_cloud_data_create_dataset.txt
	@echo "retrieve big query dataset list..."
	@$(shell sh -c "echo YnEgbHMK= | base64 -d") > tests/cloud_data/test_cloud_data_create_dataset_source.txt || :
	@echo "${TRAINING_PREFIX}" > tests/cloud_data/test_cloud_data_create_training_table.txt
	@echo "${VALIDATION_PREFIX}" > tests/cloud_data/test_cloud_data_create_validation_table.txt
	@echo "retrieve big query dataset table list..."
	@$(shell sh -c "echo YnEgbHMK= | base64 -d") ${DATASET} > tests/cloud_data/test_cloud_data_create_table_source.txt || :
	@echo "retrieve big query training table description..."
	@$(shell sh -c "echo YnEgc2hvdwo= | base64 -d") ${DATASET}.${TRAINING_PREFIX} > tests/cloud_data/test_cloud_data_table_content_training.txt || :
	@echo "retrieve big query validation table description..."
	@$(shell sh -c "echo YnEgc2hvdwo= | base64 -d") ${DATASET}.${VALIDATION_PREFIX} > tests/cloud_data/test_cloud_data_table_content_validation.txt || :
	@echo "retrieve big query training table first rows..."
	@bq query --use_legacy_sql=false "SELECT fare_amount FROM ${DATASET}.${TRAINING_PREFIX} LIMIT 10" > tests/cloud_data/test_cloud_data_bq_chunks.txt || :
# $ONLY_FOR_cloud_data_END

list:
	@echo "\nHelp for the \`taxifare-model\` package \`Makefile\`"

	@echo "\n$(ccgreen)$(fbold)PACKAGE$(ccreset)"

	@echo "\n$(ccgreen)$(fbold)TESTS$(ccreset)"

	@echo "\n    $(ccgreen)$(fbold)student rules:$(ccreset)"
	@echo "\n        $(fbold)reinstall_package$(ccreset)"
	@echo "            Install the version of the package corresponding to the challenge."
	@echo "\n        $(fbold)test_train_at_scale$(ccreset)"
	@echo "            Run the package tests."
	@echo "\n    $(ccblue)$(fbold)internal rules:$(ccreset)"
	@echo "\n        $(fbold)write_results$(ccreset)"
	@echo "            Write the test results so they can be added and committed to git."
	@echo "\n        $(fbold)pylint$(ccreset)"
	@echo "            Print a report on code style."
	@echo "\n        $(fbold)pytest$(ccreset)"
	@echo "            Run the tests and print a test report."
