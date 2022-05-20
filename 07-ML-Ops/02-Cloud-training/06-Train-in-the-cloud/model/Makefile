
default: pylint pytest

pylint:
	find . -iname "*.py" -not -path "./tests/test_*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true

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
	@env | grep -E "LOCAL_DATA_PATH|LOCAL_REGISTRY_PATH"
	@echo "\n$(ccgreen)dataset:$(ccreset)"
	@env | grep -E "DATASET_SIZE|VALIDATION_DATASET_SIZE|CHUNK_SIZE"
	@echo "\n$(ccgreen)package behavior:$(ccreset)"
	@env | grep -E "DATA_SOURCE|MODEL_TARGET"

	@echo "\n$(ccgreen)GCP:$(ccreset)"
	@env | grep -E "PROJECT|REGION"
	@echo "\n$(ccgreen)Cloud Storage:$(ccreset)"
	@env | grep -E "BUCKET_NAME|BLOB_LOCATION"

	@echo "\n$(ccgreen)Big Query:$(ccreset)"
	@env | grep -E "DATASET" | grep -Ev "DATASET_SIZE|VALIDATION_DATASET_SIZE"

	@echo "\n$(ccgreen)Compute Engine:$(ccreset)"
	@env | grep -E "INSTANCE"

reinstall_package:
	@pip uninstall -y taxifare-model
	@pip install -e .

write_results:

	@echo "verify installed packages versions"
	@pip show taxifare-model | grep 'Summary' > tests/all/test_package_version.txt || :

	@echo "retrieve compute api status..."
	@$(shell sh -c "echo Z2Nsb3VkIHNlcnZpY2VzIGxpc3QgLS1lbmFibGVkIC0tZmlsdGVyPWNvbXB1dGUuZ29vZ2xlYXBpcy5jb20K= | base64 -d") > tests/cloud_training/test_cloud_training_compute_api_enabled.txt || :
	@echo "retrieve vm list..."
	@echo "${INSTANCE}" > tests/cloud_training/test_cloud_training_create_vm.txt
	@gcloud compute instances list --filter="name=('${INSTANCE}')" > tests/cloud_training/test_cloud_training_create_vm_source.txt || :
	@echo "check instance operating system..."
	@gcloud compute ssh ${INSTANCE} --command "lsb_release -a" > tests/cloud_training/test_cloud_training_operating_system.txt 2> /dev/null || :
	@echo "retrieve vm default shell..."
	@gcloud compute ssh ${INSTANCE} --command "env | grep SHELL" > tests/cloud_training/test_cloud_training_default_shell.txt 2> /dev/null || :
	@echo "retrieve vm pyenv..."
	@gcloud compute ssh ${INSTANCE} --command "source ~/.zshrc 2> /dev/null; source ~/.zprofile 2> /dev/null; pyenv --help" > tests/cloud_training/test_cloud_training_pyenv.txt 2> /dev/null || :
	@echo "retrieve vm python version..."
	@gcloud compute ssh ${INSTANCE} --command "source ~/.zshrc 2> /dev/null; source ~/.zprofile 2> /dev/null; pyenv versions" > tests/cloud_training/test_cloud_training_python_version.txt 2> /dev/null || :
	@echo "retrieve vm gcp code auth..."
	@echo "${PROJECT}" > tests/cloud_training/test_cloud_training_project_id.txt
	@gcloud compute ssh ${INSTANCE} --command "source ~/.zshrc 2> /dev/null; source ~/.zprofile 2> /dev/null; python -c 'from google.cloud import storage; [print(b.name) for b in storage.Client().list_buckets()]'" > tests/cloud_training/test_cloud_training_list_projects.txt 2> /dev/null || :

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
	@echo "\n        $(fbold)test_train_at_scale$(ccreset)"
	@echo "            Run the package tests."
	@echo "\n        $(fbold)dev_test$(ccreset)"
	@echo "            Run the tests."

	@echo "\n    $(ccblue)$(fbold)internal rules:$(ccreset)"
	@echo "\n        $(fbold)write_results$(ccreset)"
	@echo "            Write the test results so they can be added and committed to git."
	@echo "\n        $(fbold)pylint$(ccreset)"
	@echo "            Print a report on code style."
	@echo "\n        $(fbold)pytest$(ccreset)"
	@echo "            Run the tests and print a test report."
