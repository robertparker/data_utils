SHELL := /bin/sh
DIRECTORIES = tests
TEST_COMMAND = pytest ${DIRECTORIES}

format:
	black .

format-check:
	black --check .
	flake8 .

test:
	${TEST_COMMAND}

coverage:
	coverage run -m ${TEST_COMMAND}

coverage-report:
	coverage report -m

coverage-html:
	coverage html

coverage-fast:
	coverage run -m ${TEST_COMMAND} --keepdb

coverage-fast-report: coverage-fast
	coverage report -m --skip-covered

coverage-fast-report-html: coverage-fast coverage-html
