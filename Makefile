
.PHONY: lintn all-test all-notest init test format

all-test: init test format lint

all-notest: init format lint

init:
	pip install -r requirements.txt

test:
	$(info ************  Running tests ************)
	pytest -v tests
	rm -r tests/__pycache__

format:
	$(info ************  Formatting code to standard ************)
	black . > ./Logs/format-log.txt

lint:
	$(info ************  Linting Python files ************)
	flake8 . > ./Logs/flake8lint-log.txt
	$(info ************  Linting YAML files ************)
	yamllint . > ./Logs/yamllint
