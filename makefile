SHELL:=/bin/bash
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
APP_NAME:=app
PYTHON:=python3

all: dependencies

fresh: clean dependencies

testenv: clean_testenv
	docker-compose up --build

clean_testenv:
	docker-compose down

fresh_testenv: clean_testenv testenv

venv:
	if [ ! -d $(ROOT_DIR)/env ]; then $(PYTHON) -m venv $(ROOT_DIR)/env; fi

dependencies: venv
	source $(ROOT_DIR)/env/bin/activate; yes w | python -m pip install -r $(ROOT_DIR)/requirements.txt

upgrade_dependencies: venv
	source $(ROOT_DIR)/env/bin/activate; ./bin/update_dependencies.sh $(ROOT_DIR)/requirements.txt

clean: clean_testenv
	# Remove existing environment
	rm -rf $(ROOT_DIR)/env;
	rm -rf $(ROOT_DIR)/$(APP_NAME)/*.pyc;

upgrade_models:
	rm -rf $(ROOT_DIR)/app.sqlite;
	source $(ROOT_DIR)/env/bin/activate; python manage.py db upgrade
	source $(ROOT_DIR)/env/bin/activate; python manage.py db migrate
	rm -rf $(ROOT_DIR)/app.sqlite;

init_db: dependencies
	source $(ROOT_DIR)/env/bin/activate; SECRET_KEY=TempKey python manage.py db init
	source $(ROOT_DIR)/env/bin/activate; SECRET_KEY=TempKey python manage.py db upgrade
	source $(ROOT_DIR)/env/bin/activate; SECRET_KEY=TempKey python manage.py db migrate
	rm -rf $(ROOT_DIR)/app.sqlite;
