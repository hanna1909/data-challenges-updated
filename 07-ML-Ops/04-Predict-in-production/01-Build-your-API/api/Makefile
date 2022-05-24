default: test

test:
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes --asyncio-mode=strict -W "ignore"

test_root:
	PYTHONDONTWRITEBYTECODE=1 pytest -k 'test_root' -v --color=yes --asyncio-mode=strict -W "ignore"

test_predict:
	PYTHONDONTWRITEBYTECODE=1 pytest -k 'test_predict' -v --color=yes --asyncio-mode=strict -W "ignore"
