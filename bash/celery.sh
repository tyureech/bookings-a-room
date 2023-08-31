/bin/sh

celery -A app.tasks.celery:celery_app worker -l INFO
