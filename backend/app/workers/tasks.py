
from app.workers.celery_app import celery_app


@celery_app.task(name="agentflow.ping")
def ping_task():
    return {
        "status": "success",
        "message": "Celery worker is operational"
    }

@celery_app.task(name="agentflow.fail")
def fail_task():
    """Simulate a task failure for error-handling tests."""

    raise RuntimeError("Intentional failure for testing")