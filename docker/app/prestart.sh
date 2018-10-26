#!/usr/bin/env bash

# This function waits for a service to start. Default ports can be supplies by the second argument.
wait_for_service() {
  HOSTNAME=$(urlparser hostname $1)
  PORT=$(urlparser port $1 || echo $2)
  until nc -w 5 -z $HOSTNAME $PORT
  do
    echo "Waiting for $1 to come online at $HOSTNAME $PORT"
    sleep 5
  done
}


# If there are AWS credentials configured make sure they're available to the root user as well.
# This is only needed in testing, as IAM Roles are used for production.
if [ -d /home/apprunner/.aws ]; then
  cp -Rf /home/apprunner/.aws /root/
  chown -R root:root /root/.aws
fi

# Get service hostnames from the secrets manager.
if [[ -n $AWS_SECRETS_MANAGER_CONFIG ]]; then
  if [ "$SQLALCHEMY_DATABASE_URI" == "" ]; then
    SQLALCHEMY_DATABASE_URI=$(secretcli get $AWS_SECRETS_MANAGER_CONFIG SQLALCHEMY_DATABASE_URI)
  fi
  if [ "$CELERY_BROKER" == "" ]; then
    CELERY_BROKER=$(secretcli get $AWS_SECRETS_MANAGER_CONFIG CELERY_BROKER)
  fi
fi

# Wait for configured services to become available.
if [[ -n "$CELERY_BROKER" ]]; then
  wait_for_service $CELERY_BROKER 5672
fi
if [[ -n "$SQLALCHEMY_DATABASE_URI" ]]; then
  wait_for_service $SQLALCHEMY_DATABASE_URI 5432
fi


echo 'Performing any database migrations.'
python manage.py db upgrade


echo 'Setting up initial roles and users if they do not exist.'
python manage.py add-role admin Admin

if [[ -n $ADMIN_EMAIL ]] && [[ -n $ADMIN_PASSWORD ]]; then
  python manage.py add-user $ADMIN_EMAIL $ADMIN_PASSWORD admin
fi

if [[ -n $USER_EMAIL ]] && [[ -n $USER_PASSWORD ]]; then
  python manage.py add-user $USER_EMAIL $USER_PASSWORD
fi
