
from app.workers.celery_app import celery_app


@celery_app.task(name="agentflow.ping")
def ping_task():
    return {
        "status": "success",
        "message": "Celery worker is operational"
    }
