# tedivm's flask starter app

![Screenshot](https://github.com/twintechlabs/flaskdash/blob/master/app/static/images/screenshot.png)

This code base serves as starting point for writing your next Flask application.

This package is designed to allow developers to start working on their specific features immediately while also making it simple to deploy the project into production. It contains a number of configured extensions and libraries as well as unique features specifically built for this package. It also is completely dockerized, with both a docker-compose testenv and the ability to easily make images off of the application for pushing into production.

## Rob's Awesome Template

If you like this project you may also like my latest template, [Rob's Awesome Python Template](https://github.com/tedivm/robs_awesome_python_template). It is updated with modern best practices and a variety of optional services.

## Code characteristics

* Tested on Python 3.3, 3.4, 3.5, 3.6, and 3.7
* Complete docker environment.
* Images for both the web application and the celery worker.
* Full user management system.
* Server side session storage.
* An API system with API tokens and route decorators.
* Well organized directories with lots of comments.
* Includes test framework (`py.test` and `tox`)
* Includes database migration framework (`alembic`, using `Flask-Migrate`)
* Sends error emails to admins for unhandled exceptions

## Configured Extensions and Libraries

With thanks to the following Flask extensions and libraries:

* [Beaker](https://beaker.readthedocs.io/en/latest/) for caching and session management.
* [Celery](http://www.celeryproject.org/) for running asynchronous tasks on worker nodes.
* [Click](https://click.palletsprojects.com/) for the creation of command line tools.
* [Flask](http://flask.pocoo.org/) the microframework framework which holds this all together.
* [Flask-Login](https://flask-login.readthedocs.io/) allows users to login and signout.
* [Flask-Migrate](https://flask-migrate.readthedocs.io/) integrates [Alembic](http://alembic.zzzcomputing.com/) into Flask to handle database versioning.
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org) integrates [SQLAlchemy](https://www.sqlalchemy.org/) into Flask for database modeling and access.
* [Flask-User](http://flask-user.readthedocs.io/en/v0.6/) adds user management and authorization features.
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) integrates [WTForms](https://wtforms.readthedocs.io) into Flask to handle form creation and validation.

In addition the front end uses the open source versions of:

* [Bootstrap](https://getbootstrap.com/)
* [CoreUI](https://coreui.io/)
* [Font Awesome](https://fontawesome.com/)


## Unique Features

* Database or LDAP Authentication - Applications built with this project can use the standard database backed users or can switch to LDAP authentication with a few configuration settings.

* API Authentication and Authorization - this project can allow people with the appropriate role to generate API Keys, which in turn can be used with the `roles_accepted_api` decorator to grant API access to specific routes.

* Versatile Configuration System - this project can be configured with a combination of configuration files, AWS Secrets Manager configuration, and environmental variables. This allows base settings to be built into the deployment, secrets to be managed securely, and any configuration value to be overridden by environmental variables.

* A `makefile` with a variety of options to make common tasks easier to accomplish.

* A [Celery](http://www.celeryproject.org/) based asynchronous task management system. This is extremely useful for long running tasks- they can be triggered in the web interface and then run on a worker node and take as long as they need to complete.


## Setting up a development environment

First we recommend either cloning this repository with the "Use this template" button on Github.


We assume that you have `make` and `docker`.

    # Clone the code repository into ~/dev/my_app
    mkdir -p ~/dev
    cd ~/dev
    git clone https://github.com/tedivm/tedivms-flask my_app
    cd my_app

    # For the first run, and only the first run, we need to create the first round of SQLAlchemy models.
    make init_db

    # Create the 'my_app' virtual environment and start docker containers
    make testenv

    # Restart docker app container
    docker-compose restart app

    # Start a shell in the container running the application
    docker-compose exec app /bin/bash


## Configuration

### Application configuration

To set default configuration values on the application level- such as the application name and author- edit `./app/settings.py`. This should be done as a first step whenever using this application template.

### Configuration File

A configuration file can be set with the environmental variable `APPLICATION_SETTINGS`.

### AWS Secrets Manager

Configuration can be loaded from the AWS Secrets Manager by setting the environmental variables `AWS_SECRETS_MANAGER_CONFIG` and `AWS_SECRETS_REGION`.

### Environmental Variables

Any environmental variables that have the same name as a configuration value in this application will automatically get loaded into the app's configuration.

### Configuring LDAP

Any installation can run with LDAP as its backend with these settings.

```
USER_LDAP=true
LDAP_HOST=ldap://ldap
LDAP_BIND_DN=cn=admin,dc=example,dc=org
LDAP_BIND_PASSWORD=admin
LDAP_USERNAME_ATTRIBUTE=cn
LDAP_USER_BASE=ou=users,dc=example,dc=org
LDAP_GROUP_OBJECT_CLASS=posixGroup
LDAP_GROUP_ATTRIBUTE=cn
LDAP_GROUP_BASE=ou=groups,dc=example,dc=org
LDAP_GROUP_TO_ROLE_ADMIN=admin
LDAP_GROUP_TO_ROLE_DEV=dev
LDAP_GROUP_TO_ROLE_USER=user
LDAP_EMAIL_ATTRIBUTE=mail
```


## Initializing the Database

    # Initialize the database. This will create the `migrations` folder and is only needed once per project.
    make init_db

    # This creates a new migration. It should be run whenever you change your database models.
    make upgrade_models


## Running the app

    # Start the Flask development web server
    make testenv


Point your web browser to <http://localhost/>

You can make use of the following users:
* email `user@example.com` with password `Password1`.
* email `dev@example.com` with password `Password1`.
* email `admin@example.com` with password `Password1`.


## Running the automated tests

    # To run the test suite.
    make run_tests



## Acknowledgements

<!-- Please consider leaving this line. Thank you -->
[Flask-Dash](https://github.com/twintechlabs/flaskdash) was used as a starting point for this code repository. That project was based off of the [Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app).

## Authors

- Robert Hafner (tedivms-flask) -- tedivm@tedivm.com
* Matt Hogan (flaskdash) -- matt AT twintechlabs DOT io
* Ling Thio (flask-user) -- ling.thio AT gmail DOT com
