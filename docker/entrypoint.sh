#!/bin/bash

set -e

# Set UTF-8 encoding to address potential encoding issues in containerized environments
export LANG=${LANG:-en_US.UTF-8}
export LC_ALL=${LC_ALL:-en_US.UTF-8}
export PYTHONIOENCODING=${PYTHONIOENCODING:-utf-8}

if [[ "${MODE}" == "worker" ]]; then
  
  CONCURRENCY_OPTION="-c ${CELERY_WORKER_AMOUNT:-1}"
  WORKER_POOL="${CELERY_WORKER_POOL:-${CELERY_WORKER_CLASS:-gevent}}"

  exec celery -A app.celery worker -P ${WORKER_POOL} $CONCURRENCY_OPTION \
    --max-tasks-per-child ${MAX_TASKS_PER_CHILD:-50} --loglevel ${LOG_LEVEL:-INFO} \
    --prefetch-multiplier=${CELERY_PREFETCH_MULTIPLIER:-1}

else
  if [[ "${DEBUG}" == "true" ]]; then
    exec flask run --host=${APP_BIND_ADDRESS:-0.0.0.0} --port=${APP_PORT:-5001} --debug
  else
    exec gunicorn \
      --bind "${APP_BIND_ADDRESS:-0.0.0.0}:${APP_PORT:-5001}" \
      --workers ${SERVER_WORKER_AMOUNT:-1} \
      --worker-class ${SERVER_WORKER_CLASS:-gevent} \
      --worker-connections ${SERVER_WORKER_CONNECTIONS:-10} \
      --timeout ${GUNICORN_TIMEOUT:-200} \
      app:app
  fi
fi