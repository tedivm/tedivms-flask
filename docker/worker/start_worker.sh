#!/usr/bin/env bash

wait_for_service() {
  HOSTNAME=$(urlparser hostname $1)
  PORT=$(urlparser port $1 || echo $2)
  until nc -w 5 -z $HOSTNAME $PORT
  do
    echo "Waiting for service to come online at $HOSTNAME $PORT"
    sleep 5
  done
}

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


# Add default celery concurrency options.
if [ "$CELERY_MAX_CONCURRENCY" == "" ]; then
  CELERY_MAX_CONCURRENCY='10'
fi
if [ "$CELERY_MIN_CONCURRENCY" == "" ]; then
  CELERY_MIN_CONCURRENCY='2'
fi


if [ "$DISABLE_BEAT" = "true" ]
then
  echo 'Launching celery worker without beat'
  echo "celery worker -A app.worker:celery --loglevel=info --autoscale=${CELERY_MAX_CONCURRENCY},${CELERY_MIN_CONCURRENCY}"
  celery worker -A app.worker:celery --loglevel=info --autoscale=${CELERY_MAX_CONCURRENCY},${CELERY_MIN_CONCURRENCY}
else
  echo 'Launching celery worker with beat enabled'
  rm -f ~/celerybeat-schedule
  echo "celery worker -A app.worker:celery --loglevel=info --autoscale=${CELERY_MAX_CONCURRENCY},${CELERY_MIN_CONCURRENCY}" -B -s ~/celerybeat-schedule
  celery worker -A app.worker:celery --loglevel=info --autoscale=${CELERY_MAX_CONCURRENCY},${CELERY_MIN_CONCURRENCY} -B -s ~/celerybeat-schedule
fi
