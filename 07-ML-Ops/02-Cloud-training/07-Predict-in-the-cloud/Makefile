
default: pytest

# default: pylint pytest

# pylint:
# 	find . -iname "*.py" -not -path "./tests/test_*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true

pytest:
	cd model && PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes