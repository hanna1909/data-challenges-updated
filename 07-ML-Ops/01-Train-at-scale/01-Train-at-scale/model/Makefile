
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

reinstall_package:
	@pip uninstall -y taxifare-model
	@pip install -e .

write_results:

	@echo "verify installed packages versions"
	@pip show taxifare-model | grep 'Summary' > tests/all/test_package_version.txt || :

	@python -m tests.notebook.write_train

list:
	@echo "\nHelp for the \`taxifare-model\` package \`Makefile\`"

	@echo "\n$(ccgreen)$(fbold)PACKAGE$(ccreset)"

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

	@echo "\n    $(ccgreen)$(fbold)internal rules:$(ccreset)"
	@echo "\n        $(fbold)write_results$(ccreset)"
	@echo "            Write the test results so they can be added and committed to git."
	@echo "\n        $(fbold)pylint$(ccreset)"
	@echo "            Print a report on code style."
	@echo "\n        $(fbold)pytest$(ccreset)"
	@echo "            Run the tests and print a test report."
