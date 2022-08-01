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

test_cloud_training: test_gcp_setup test_gcp_project test_gcp_bucket test_big_query test_cloud_data

test_gcp_setup:
	@TEST_ENV=development pytest \
	tests/setup/test_gcp_setup.py::TestGcpSetup::test_setup_key_env \
	tests/setup/test_gcp_setup.py::TestGcpSetup::test_setup_key_path \
	tests/setup/test_gcp_setup.py::TestGcpSetup::test_code_get_project

test_gcp_project:
	@TEST_ENV=development pytest \
	tests/setup/test_gcp_setup.py::TestGcpSetup::test_setup_project_id

test_gcp_bucket:
	@TEST_ENV=development pytest \
	tests/setup/test_gcp_setup.py::TestGcpSetup::test_setup_bucket_exists \
	tests/setup/test_gcp_setup.py::TestGcpSetup::test_setup_bucket_name

test_big_query:
	@TEST_ENV=development pytest \
	tests/cloud_data/test_cloud_data.py::TestCloudData::test_big_query_dataset_variable_exists \
	tests/cloud_data/test_cloud_data.py::TestCloudData::test_cloud_data_create_dataset \
	tests/cloud_data/test_cloud_data.py::TestCloudData::test_cloud_data_create_table \
	tests/cloud_data/test_cloud_data.py::TestCloudData::test_cloud_data_table_content

test_cloud_data:
	@TEST_ENV=development pytest tests/cloud_data/test_cloud_data.py::TestCloudData::test_cloud_data_bq_chunks

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

show_env:
	@echo "\nEnvironment variables used by the \`taxifare\` package loaded by \`direnv\` from your \`.env\` located at:"
	@echo ${DIRENV_DIR}

	@echo "\n$(ccgreen)local storage:$(ccreset)"
	@env | grep -E "LOCAL_DATA_PATH|LOCAL_REGISTRY_PATH" || :
	@echo "\n$(ccgreen)dataset:$(ccreset)"
	@env | grep -E "DATASET_SIZE|VALIDATION_DATASET_SIZE|CHUNK_SIZE" || :
	@echo "\n$(ccgreen)package behavior:$(ccreset)"
	@env | grep -E "DATA_SOURCE|MODEL_TARGET" || :

	@echo "\n$(ccgreen)GCP:$(ccreset)"
	@env | grep -E "PROJECT|REGION" || :

	@echo "\n$(ccgreen)Big Query:$(ccreset)"
	@env | grep -E "DATASET" | grep -Ev "DATASET_SIZE|VALIDATION_DATASET_SIZE" || :\

	@echo "\n$(ccgreen)Compute Engine:$(ccreset)"
	@env | grep -E "INSTANCE" || :

reinstall_package:
	@pip uninstall -y taxifare || :
	@pip install -e .

list:
	@echo "\nHelp for the \`taxifare\` package \`Makefile\`"

	@echo "\n$(ccgreen)$(fbold)PACKAGE$(ccreset)"

	@echo "\n    $(ccgreen)$(fbold)environment rules:$(ccreset)"
	@echo "\n        $(fbold)show_env$(ccreset)"
	@echo "            Show the environment variables used by the package by category."

	@echo "\n    $(ccgreen)$(fbold)run rules:$(ccreset)"
	@echo "\n        $(fbold)run_model$(ccreset)"
	@echo "            Run the package (\`taxifare.interface.main\` module)."

	@echo "\n$(ccgreen)$(fbold)TESTS$(ccreset)"

	@echo "\n    $(ccgreen)$(fbold)student rules:$(ccreset)"
	@echo "\n        $(fbold)reinstall_package$(ccreset)"
	@echo "            Install the version of the package corresponding to the challenge."
	@echo "\n        $(fbold)test_cloud_training$(ccreset)"
	@echo "            Run the tests."
