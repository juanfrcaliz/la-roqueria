SRC_DIR=src
TEST_DIR=tests

install-dev:
	@pip install -r requirements-dev.txt

format:
	@black ${SRC_DIR} ${TEST_DIR}
	@isort ${SRC_DIR} ${TEST_DIR}

test:
	@python -m pytest
