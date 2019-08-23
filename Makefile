
.PHONY: lint all-test all-notest init test format cleanup

prep-test: init test format lint cleanup
prep-notest: init format lint cleanup

init:
	pip install -r requirements.txt

test:
	$(info ************  Running tests ************)
	pytest -v tests

format:
	$(info ************  Formatting code to standard ************)
	black . > ./Logs/format-log.txt

lint:
	$(info ************  Linting Python files ************)
	flake8 . > ./Logs/flake8lint-log.txt
	$(info ************  Linting YAML files ************)
	yamllint . > ./Logs/yamllint

cleanup:
	rm -r tests/__pycache__
	rm -r .pytest_cache

