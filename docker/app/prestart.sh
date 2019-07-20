#!/usr/bin/env bash

# This function waits for a service to start. Default ports can be supplies by the second argument.
wait_for_service() {
  HOSTNAME=$(urlparser hostname $1)
  PORT=$(urlparser port $1 || echo $2)
  until nc -w 5 -z $HOSTNAME $PORT
  do
    echo "Waiting for service to come online at $HOSTNAME $PORT"
    sleep 5
  done
}

echo 'Setting up configuration and waiting for services.'

# If there are AWS credentials configured make sure they're available to the root user as well.
# This is only needed in testing, as IAM Roles are used for production.
if [ -d /home/apprunner/.aws ]; then
  cp -Rf /home/apprunner/.aws /root/
  chown -R root:root /root/.aws
fi

# Get service hostnames from the secrets manager.
if [ ! -z "$AWS_SECRETS_MANAGER_CONFIG" ]; then
  if [ -z "$SQLALCHEMY_DATABASE_URI" ]; then
    SQLALCHEMY_DATABASE_URI=$(secretcli get $AWS_SECRETS_MANAGER_CONFIG SQLALCHEMY_DATABASE_URI)
  fi
  if [ -z "$CELERY_BROKER" ]; then
    CELERY_BROKER=$(secretcli get $AWS_SECRETS_MANAGER_CONFIG CELERY_BROKER)
  fi
fi


# Wait for configured services to become available.
if [ ! -z "$CELERY_BROKER" ]; then
  wait_for_service $CELERY_BROKER 5672
fi
if [ ! -z "$SQLALCHEMY_DATABASE_URI" ]; then
  wait_for_service $SQLALCHEMY_DATABASE_URI 5432
fi

set -e
echo 'Performing any database migrations.'
python manage.py db upgrade

if [ ! -f ~/.hasrun ]; then
  echo 'Setting up initial roles and users if they do not exist.'
  python manage.py add-role admin Admin
  python manage.py add-role dev Developer
  python manage.py add-role user User

  if [ ! -z "$ADMIN_USERNAME" ] && [ ! -z "$ADMIN_EMAIL" ] && [ ! -z "$ADMIN_PASSWORD" ]; then
    python manage.py add-user $ADMIN_USERNAME $ADMIN_EMAIL $ADMIN_PASSWORD admin
  fi

  if [ ! -z "$DEV_USERNAME" ] && [ ! -z "$DEV_EMAIL" ] && [ ! -z "$DEV_PASSWORD" ]; then
    python manage.py add-user $DEV_USERNAME $DEV_EMAIL $DEV_PASSWORD dev
  fi

  if [ ! -z "$USER_USERNAME" ] && [ ! -z "$USER_EMAIL" ] && [ ! -z "$USER_PASSWORD" ]; then
    python manage.py add-user $USER_USERNAME $USER_EMAIL $USER_PASSWORD user
  fi

  touch ~/.hasrun
fi
