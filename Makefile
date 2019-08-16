
.PHONY: lintn all-test all-notest init test

all-test: init test lint

all-notest: init lint

init:
	pip install -r requirements.txt

test:
	py.test tests


lint:
	$(info ************  Linting Python files ************)
	flake8 . > ./Logs/lint-log.txt
