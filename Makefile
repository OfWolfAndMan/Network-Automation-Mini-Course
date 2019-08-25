
.PHONY: lint all-test all-notest init test format prep-cleanup cleanup deploy stop-api destroy-lab

prep-test: init test format lint prep-cleanup
prep-notest: init format lint prep-cleanup

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

stop-api: server.PID
	kill `cat $<` && rm $<

deploy:
# 	export FLASK_ENV=development && \
#  	export FLASK_APP=./APIs/app.py && \
#  	nohup flask run & > server.PID
	python3 ./APIs/app.py & echo $$! > server.PID
	sleep 2
	python3 ./deploy-lab.py "My New Lab"

destroy-lab:
	python3 ./destroy-lab.py "My New Lab"
