from fastapi import APIRouter, Response
from celery.result import AsyncResult

from app.workers.celery_app import celery_app
from app.workers.tasks import ping_task, fail_task


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/fail")
async def submit_fail_task():
    """Submit a task that intentionally fails."""

    task = fail_task.delay()

    return {
        "task_id": task.id,
        "status": "submitted",
        "message": "Failing task submitted successfully",
    }

@router.get("/{task_id}")
async def get_task_status(task_id: str, response: Response):
    """Retrieve the status and result of a Celery task."""

    task_result = AsyncResult(task_id, app=celery_app)

    response_data = {
        "task_id": task_id,
        "status": task_result.status.lower(),
        "result": None,
        "error": None,
        "message": None,
    }

    if task_result.successful():
        response_data["result"] = task_result.result

    elif task_result.failed():
        response.status_code = 500
        response_data["error"] = "Task execution failed."
        response_data["message"] = "Check worker logs for details."

    elif task_result.status == "PENDING":
        response_data["message"] = (
            "Task is pending or the task ID is unknown."
        )

    return response_data
