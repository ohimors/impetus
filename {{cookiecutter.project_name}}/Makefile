SERVICE := $(shell grep 'name=' setup.py | head -n1 | cut -d '=' -f 2 | sed "s/['\", ]//g")
PROJECT := $(SERVICE)_project
PYTHON := $(PWD)/venv/bin/python3
MANAGE := $(PROJECT)/manage.py
DOCKER_COMPOSE ?= docker-compose
DOCKER_VOLUME := /usr/local/lib/python3.6/site-packages/{{cookiecutter.application_name}}-0.0.0-py3.6.egg/{{cookiecutter.application_name}}


# Disable pylint checks:
# 	E1103 no member: false-positives in cases where methods / attributes
#					are defined at runtime
# 				   for ex. "Class 'Permission' has no 'objects' member"
PYLINT_DISABLE :=  E1103
# Enable pylint checks that are not errors:
# 	C0111 missing docsting: enable for all our code except for tests
# 	W0102 dangerous default value as argument
# 	W0311 bad indentation
# 	W0611 unused import
# 	W0612 unused variable
# 	W0613 unused argument
# 	W1201 specify string format arguments as logging function parameters
# 	W1505 deprecated method
PYLINT_ENABLE_FOR_TESTS := W0102,W0311,W0611,W0612,W1201,W1505
PYLINT_ENABLE := C0111,W0613,$(PYLINT_ENABLE_FOR_TESTS)

# print out more info about errors: full error identifier (msg_id), etc
PYLINT_OUTPUT_FORMAT = '{msg_id}:{line:3d},{column}: {obj}: {msg} ({symbol})'

PYLINT_OPTIONS = --errors-only --disable=$(PYLINT_DISABLE) --enable=$(PYLINT_ENABLE) --ignore=migrations,tests --msg-template=$(PYLINT_OUTPUT_FORMAT)
PYLINT_OPTIONS_FOR_TESTS_FOLDER = --errors-only --disable=$(PYLINT_DISABLE) --enable=$(PYLINT_ENABLE_FOR_TESTS) --msg-template=$(PYLINT_OUTPUT_FORMAT)


define initdb
	which mysql && which mysql_config || { \
		echo "MySQL installation with binary in PATH required"; \
		exit 1; \
	}
	@echo "CREATE DATABASE IF NOT EXISTS $(SERVICE) DEFAULT CHARACTER SET utf8mb4" \
		"DEFAULT COLLATE utf8mb4_general_ci;" \
		"GRANT ALL ON $(SERVICE).* TO 'socialcode'@'localhost' IDENTIFIED BY 'edoclaicos';" \
		"GRANT ALL ON test_$(SERVICE).* TO 'socialcode'@'localhost' IDENTIFIED BY 'edoclaicos';" \
		"FLUSH PRIVILEGES;" | mysql -u root
endef

.PHONY: create_db
create_db:
	$(initdb)

.PHONY: drop_db
drop_db:
	@echo "drop database  $(SERVICE)" | mysql -u root

venv: Makefile requirements.txt
	virtualenv -p python3 venv --prompt="{$(SERVICE)}"
	$(PWD)/venv/bin/pip install --upgrade pip
	$(PWD)/venv/bin/pip install -r requirements.txt
	$(PWD)/venv/bin/django-admin.py startproject $(PROJECT) || echo "$(PROJECT) already created"
	$(PYTHON) setup.py develop
	@touch -c venv

.PHONY: prereqs
prereqs: venv
	$(initdb)

.PHONY: makemigrations
makemigrations:
	$(PYTHON) $(MANAGE) makemigrations $(SERVICE) --settings=$(SERVICE).dev_settings
	git add $(SERVICE)/migrations/*

.PHONY: migrate
migrate:
	$(PYTHON) $(MANAGE) migrate --settings=$(SERVICE).dev_settings

.PHONY: shell
shell:
	$(PYTHON) $(MANAGE) shell --settings=$(SERVICE).dev_settings

.PHONY: dbshell
dbshell:
	$(PYTHON) $(MANAGE) dbshell --settings=$(SERVICE).dev_settings

.PHONY: shell-docker
shell-docker:
	$(DOCKER_COMPOSE) build web
	$(DOCKER_COMPOSE) run web django-admin shell

.PHONY: style
style:
	$(DOCKER_COMPOSE) build web
	$(DOCKER_COMPOSE) run --no-deps web pycodestyle --max-line-length=500 $(DOCKER_VOLUME) --exclude=$(DOCKER_VOLUME)/migrations/
	$(DOCKER_COMPOSE) run --no-deps web pylint $(DOCKER_VOLUME) $(PYLINT_OPTIONS)
	$(DOCKER_COMPOSE) run --no-deps web pylint $(DOCKER_VOLUME)/tests $(PYLINT_OPTIONS_FOR_TESTS_FOLDER)

.PHONY: test
test:
	$(DOCKER_COMPOSE) down --remove-orphans
	$(DOCKER_COMPOSE) build
	$(DOCKER_COMPOSE) run -e TEST=true web --wait 'tcp://database:3306' --timeout 60s django-admin test --noinput $(SERVICE)

.PHONY: web
web:
	VERSION=`git describe --tags --match '*[0-9]*.[0-9]*.[0-9]*'` $(DOCKER_COMPOSE) up --build web

# Useful with pdb.set_trace() for debugging.
.PHONY: dev-server
dev-server:
	$(PYTHON) $(MANAGE) runserver --settings=$(SERVICE).dev_settings

.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down --remove-orphans
	rm -rf *.egg-info venv build dist $(PROJECT)
