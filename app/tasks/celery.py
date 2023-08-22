from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost", include=["app.tasks.tasks"])
