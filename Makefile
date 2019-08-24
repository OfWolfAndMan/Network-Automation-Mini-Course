
.PHONY: lint all-test all-notest init test format prep-cleanup cleanup implement start-api stop-api deploy-lab destroy-lab

prep-test: init test format lint prep-cleanup
prep-notest: init format lint prep-cleanup

implement: deploy-lab start-api
cleanup: stop-api destroy-lab

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

prep-cleanup:
	rm -r tests/__pycache__
	rm -r .pytest_cache

start-api:
	{ python3 ./APIs/app.py & echo $$! > server.PID; } &

stop-api: server.PID
	kill `cat $<` && rm $<

deploy-lab:
	python3 ./EVE_NG/deploy-lab.py "My New Lab"

destroy-lab:
	python3 ./EVE_NG/destroy-lab.py "My New Lab"
