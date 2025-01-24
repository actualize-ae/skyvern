import datetime
import hashlib
import os
import uuid
from enum import Enum
from typing import Annotated, Any

import structlog
import yaml
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Header,
    HTTPException,
    Query,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from sqlalchemy.exc import OperationalError

from skyvern import analytics
from skyvern.config import settings
from skyvern.exceptions import StepNotFound
from skyvern.forge import app
from skyvern.forge.prompts import prompt_engine
from skyvern.forge.sdk.api.aws import aws_client
from skyvern.forge.sdk.api.llm.exceptions import LLMProviderError
from skyvern.forge.sdk.artifact.models import Artifact
from skyvern.forge.sdk.core import skyvern_context
from skyvern.forge.sdk.core.permissions.permission_checker_factory import PermissionCheckerFactory
from skyvern.forge.sdk.core.security import generate_skyvern_signature
from skyvern.forge.sdk.db.enums import OrganizationAuthTokenType
from skyvern.forge.sdk.executor.factory import AsyncExecutorFactory
from skyvern.forge.sdk.models import Step
from skyvern.forge.sdk.schemas.ai_suggestions import AISuggestionBase, AISuggestionRequest
from skyvern.forge.sdk.schemas.observers import ObserverTaskRequest
from skyvern.forge.sdk.schemas.organizations import (
    GetOrganizationAPIKeysResponse,
    GetOrganizationsResponse,
    Organization,
    OrganizationUpdate,
)
from skyvern.forge.sdk.schemas.task_generations import GenerateTaskRequest, TaskGeneration, TaskGenerationBase
from skyvern.forge.sdk.schemas.tasks import (
    CreateTaskResponse,
    OrderBy,
    SortDirection,
    Task,
    TaskRequest,
    TaskResponse,
    TaskStatus,
)
from skyvern.forge.sdk.schemas.workflow_runs import WorkflowRunTimeline
from skyvern.forge.sdk.services import observer_service, org_auth_service
from skyvern.forge.sdk.workflow.exceptions import (
    FailedToCreateWorkflow,
    FailedToUpdateWorkflow,
    WorkflowParameterMissingRequiredValue,
)
from skyvern.forge.sdk.workflow.models.workflow import (
    RunWorkflowResponse,
    Workflow,
    WorkflowRequestBody,
    WorkflowRun,
    WorkflowRunStatus,
    WorkflowRunStatusResponse,
)
from skyvern.forge.sdk.workflow.models.yaml import WorkflowCreateYAMLRequest
from skyvern.webeye.actions.actions import Action
from skyvern.webeye.schemas import BrowserSessionResponse

base_router = APIRouter()
v2_router = APIRouter()

LOG = structlog.get_logger()


@base_router.post("/webhook", tags=["server"])
@base_router.post("/webhook/", tags=["server"], include_in_schema=False)
async def webhook(
    request: Request,
    x_skyvern_signature: Annotated[str | None, Header()] = None,
    x_skyvern_timestamp: Annotated[str | None, Header()] = None,
) -> Response:
    analytics.capture("skyvern-oss-agent-webhook-received")
    payload = await request.body()

    if not x_skyvern_signature or not x_skyvern_timestamp:
        LOG.error(
            "Webhook signature or timestamp missing",
            x_skyvern_signature=x_skyvern_signature,
            x_skyvern_timestamp=x_skyvern_timestamp,
            payload=payload,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing webhook signature or timestamp",
        )

    generated_signature = generate_skyvern_signature(
        payload.decode("utf-8"),
        settings.SKYVERN_API_KEY,
    )

    LOG.info(
        "Webhook received",
        x_skyvern_signature=x_skyvern_signature,
        x_skyvern_timestamp=x_skyvern_timestamp,
        payload=payload,
        generated_signature=generated_signature,
        valid_signature=x_skyvern_signature == generated_signature,
    )
    return Response(content="webhook validation", status_code=200)


@base_router.get("/heartbeat", tags=["server"])
@base_router.get("/heartbeat/", tags=["server"], include_in_schema=False)
async def check_server_status() -> Response:
    """
    Check if the server is running.
    """
    return Response(content="Server is running.", status_code=200)


@base_router.post("/tasks", tags=["agent"], response_model=CreateTaskResponse)
@base_router.post(
    "/tasks/",
    tags=["agent"],
    response_model=CreateTaskResponse,
    include_in_schema=False,
)
async def create_agent_task(
    request: Request,
    background_tasks: BackgroundTasks,
    task: TaskRequest,
    current_org: Organization = Depends(org_auth_service.get_current_org),
    x_api_key: Annotated[str | None, Header()] = None,
    x_max_steps_override: Annotated[int | None, Header()] = None,
) -> CreateTaskResponse:
    analytics.capture("skyvern-oss-agent-task-create", data={"url": task.url})
    await PermissionCheckerFactory.get_instance().check(current_org)

    created_task = await app.agent.create_task(task, current_org.organization_id)
    if x_max_steps_override:
        LOG.info(
            "Overriding max steps per run",
            max_steps_override=x_max_steps_override,
            organization_id=current_org.organization_id,
            task_id=created_task.task_id,
        )
    await AsyncExecutorFactory.get_executor().execute_task(
        request=request,
        background_tasks=background_tasks,
        task_id=created_task.task_id,
        organization_id=current_org.organization_id,
        max_steps_override=x_max_steps_override,
        browser_session_id=task.browser_session_id,
        api_key=x_api_key,
    )
    return CreateTaskResponse(task_id=created_task.task_id)


@base_router.post(
    "/tasks/{task_id}/steps/{step_id}",
    tags=["agent"],
    response_model=Step,
    summary="Executes a specific step",
)
@base_router.post(
    "/tasks/{task_id}/steps/{step_id}/",
    tags=["agent"],
    response_model=Step,
    summary="Executes a specific step",
    include_in_schema=False,
)
@base_router.post(
    "/tasks/{task_id}/steps",
    tags=["agent"],
    response_model=Step,
    summary="Executes the next step",
)
@base_router.post(
    "/tasks/{task_id}/steps/",
    tags=["agent"],
    response_model=Step,
    summary="Executes the next step",
    include_in_schema=False,
)
async def execute_agent_task_step(
    task_id: str,
    step_id: str | None = None,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Response:
    analytics.capture("skyvern-oss-agent-task-step-execute")
    task = await app.DATABASE.get_task(task_id, organization_id=current_org.organization_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No task found with id {task_id}",
        )
    # An empty step request means that the agent should execute the next step for the task.
    if not step_id:
        step = await app.DATABASE.get_latest_step(task_id=task_id, organization_id=current_org.organization_id)
        if not step:
            raise StepNotFound(current_org.organization_id, task_id)
        LOG.info(
            "Executing latest step since no step_id was provided",
            task_id=task_id,
            step_id=step.step_id,
            step_order=step.order,
            step_retry=step.retry_index,
        )
        if not step:
            LOG.error(
                "No steps found for task",
                task_id=task_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No steps found for task {task_id}",
            )
    else:
        step = await app.DATABASE.get_step(task_id, step_id, organization_id=current_org.organization_id)
        if not step:
            raise StepNotFound(current_org.organization_id, task_id, step_id)
        LOG.info(
            "Executing step",
            task_id=task_id,
            step_id=step.step_id,
            step_order=step.order,
            step_retry=step.retry_index,
        )
        if not step:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No step found with id {step_id}",
            )
    step, _, _ = await app.agent.execute_step(current_org, task, step)
    return Response(
        content=step.model_dump_json(exclude_none=True) if step else "",
        status_code=200,
        media_type="application/json",
    )


@base_router.get("/tasks/{task_id}", response_model=TaskResponse)
@base_router.get("/tasks/{task_id}/", response_model=TaskResponse, include_in_schema=False)
async def get_task(
    task_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> TaskResponse:
    analytics.capture("skyvern-oss-agent-task-get")
    task_obj = await app.DATABASE.get_task(task_id, organization_id=current_org.organization_id)
    if not task_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found {task_id}",
        )

    # get latest step
    latest_step = await app.DATABASE.get_latest_step(task_id, organization_id=current_org.organization_id)
    if not latest_step:
        return await app.agent.build_task_response(task=task_obj)

    failure_reason: str | None = None
    if task_obj.status == TaskStatus.failed and (latest_step.output or task_obj.failure_reason):
        failure_reason = ""
        if task_obj.failure_reason:
            failure_reason += task_obj.failure_reason or ""
        if latest_step.output is not None and latest_step.output.actions_and_results is not None:
            action_results_string: list[str] = []
            for action, results in latest_step.output.actions_and_results:
                if len(results) == 0:
                    continue
                if results[-1].success:
                    continue
                action_results_string.append(f"{action.action_type} action failed.")

            if len(action_results_string) > 0:
                failure_reason += "(Exceptions: " + str(action_results_string) + ")"
    return await app.agent.build_task_response(
        task=task_obj, last_step=latest_step, failure_reason=failure_reason, need_browser_log=True
    )


@base_router.post("/tasks/{task_id}/cancel")
@base_router.post("/tasks/{task_id}/cancel/", include_in_schema=False)
async def cancel_task(
    task_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
    x_api_key: Annotated[str | None, Header()] = None,
) -> None:
    analytics.capture("skyvern-oss-agent-task-get")
    task_obj = await app.DATABASE.get_task(task_id, organization_id=current_org.organization_id)
    if not task_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found {task_id}",
        )
    task = await app.agent.update_task(task_obj, status=TaskStatus.canceled)
    # get latest step
    latest_step = await app.DATABASE.get_latest_step(task_id, organization_id=current_org.organization_id)
    # retry the webhook
    await app.agent.execute_task_webhook(task=task, last_step=latest_step, api_key=x_api_key)


@base_router.post("/workflows/runs/{workflow_run_id}/cancel")
@base_router.post("/workflows/runs/{workflow_run_id}/cancel/", include_in_schema=False)
async def cancel_workflow_run(
    workflow_run_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
    x_api_key: Annotated[str | None, Header()] = None,
) -> None:
    workflow_run = await app.DATABASE.get_workflow_run(
        workflow_run_id=workflow_run_id,
        organization_id=current_org.organization_id,
    )
    if not workflow_run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow run not found {workflow_run_id}",
        )
    await app.WORKFLOW_SERVICE.mark_workflow_run_as_canceled(workflow_run_id)
    await app.WORKFLOW_SERVICE.execute_workflow_webhook(workflow_run, api_key=x_api_key)


@base_router.post(
    "/tasks/{task_id}/retry_webhook",
    tags=["agent"],
    response_model=TaskResponse,
)
@base_router.post(
    "/tasks/{task_id}/retry_webhook/",
    tags=["agent"],
    response_model=TaskResponse,
    include_in_schema=False,
)
async def retry_webhook(
    task_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
    x_api_key: Annotated[str | None, Header()] = None,
) -> TaskResponse:
    analytics.capture("skyvern-oss-agent-task-retry-webhook")
    task_obj = await app.DATABASE.get_task(task_id, organization_id=current_org.organization_id)
    if not task_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found {task_id}",
        )

    # get latest step
    latest_step = await app.DATABASE.get_latest_step(task_id, organization_id=current_org.organization_id)
    if not latest_step:
        return await app.agent.build_task_response(task=task_obj)

    # retry the webhook
    await app.agent.execute_task_webhook(task=task_obj, last_step=latest_step, api_key=x_api_key)

    return await app.agent.build_task_response(task=task_obj, last_step=latest_step)


@base_router.get("/internal/tasks/{task_id}", response_model=list[Task])
@base_router.get("/internal/tasks/{task_id}/", response_model=list[Task], include_in_schema=False)
async def get_task_internal(
    task_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Response:
    """
    Get all tasks.
    :param page: Starting page, defaults to 1
    :param page_size:
    :return: List of tasks with pagination without steps populated. Steps can be populated by calling the
        get_agent_task endpoint.
    """
    analytics.capture("skyvern-oss-agent-task-get-internal")
    task = await app.DATABASE.get_task(task_id, organization_id=current_org.organization_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found {task_id}",
        )
    return ORJSONResponse(task.model_dump())


@base_router.get("/tasks", tags=["agent"], response_model=list[Task])
@base_router.get("/tasks/", tags=["agent"], response_model=list[Task], include_in_schema=False)
async def get_agent_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    task_status: Annotated[list[TaskStatus] | None, Query()] = None,
    workflow_run_id: Annotated[str | None, Query()] = None,
    current_org: Organization = Depends(org_auth_service.get_current_org),
    only_standalone_tasks: bool = Query(False),
    application: Annotated[str | None, Query()] = None,
    sort: OrderBy = Query(OrderBy.created_at),
    order: SortDirection = Query(SortDirection.desc),
) -> Response:
    """
    Get all tasks.
    :param page: Starting page, defaults to 1
    :param page_size: Page size, defaults to 10
    :param task_status: Task status filter
    :param workflow_run_id: Workflow run id filter
    :param only_standalone_tasks: Only standalone tasks, tasks which are part of a workflow run will be filtered out
    :param order: Direction to sort by, ascending or descending
    :param sort: Column to sort by, created_at or modified_at
    :return: List of tasks with pagination without steps populated. Steps can be populated by calling the
        get_agent_task endpoint.
    """
    analytics.capture("skyvern-oss-agent-tasks-get")
    if only_standalone_tasks and workflow_run_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="only_standalone_tasks and workflow_run_id cannot be used together",
        )
    tasks = await app.DATABASE.get_tasks(
        page,
        page_size,
        task_status=task_status,
        workflow_run_id=workflow_run_id,
        organization_id=current_org.organization_id,
        only_standalone_tasks=only_standalone_tasks,
        order=order,
        order_by_column=sort,
        application=application,
    )
    return ORJSONResponse([(await app.agent.build_task_response(task=task)).model_dump() for task in tasks])


@base_router.get("/internal/tasks", tags=["agent"], response_model=list[Task])
@base_router.get(
    "/internal/tasks/",
    tags=["agent"],
    response_model=list[Task],
    include_in_schema=False,
)
async def get_agent_tasks_internal(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Response:
    """
    Get all tasks.
    :param page: Starting page, defaults to 1
    :param page_size: Page size, defaults to 10
    :return: List of tasks with pagination without steps populated. Steps can be populated by calling the
        get_agent_task endpoint.
    """
    analytics.capture("skyvern-oss-agent-tasks-get-internal")
    tasks = await app.DATABASE.get_tasks(
        page, page_size, workflow_run_id=None, organization_id=current_org.organization_id
    )
    return ORJSONResponse([task.model_dump() for task in tasks])


@base_router.get("/tasks/{task_id}/steps", tags=["agent"], response_model=list[Step])
@base_router.get(
    "/tasks/{task_id}/steps/",
    tags=["agent"],
    response_model=list[Step],
    include_in_schema=False,
)
async def get_agent_task_steps(
    task_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Response:
    """
    Get all steps for a task.
    :param task_id:
    :return: List of steps for a task with pagination.
    """
    analytics.capture("skyvern-oss-agent-task-steps-get")
    steps = await app.DATABASE.get_task_steps(task_id, organization_id=current_org.organization_id)
    return ORJSONResponse([step.model_dump(exclude_none=True) for step in steps])


class EntityType(str, Enum):
    STEP = "step"
    TASK = "task"
    WORKFLOW_RUN = "workflow_run"
    WORKFLOW_RUN_BLOCK = "workflow_run_block"
    OBSERVER_THOUGHT = "observer_thought"


entity_type_to_param = {
    EntityType.STEP: "step_id",
    EntityType.TASK: "task_id",
    EntityType.WORKFLOW_RUN: "workflow_run_id",
    EntityType.WORKFLOW_RUN_BLOCK: "workflow_run_block_id",
    EntityType.OBSERVER_THOUGHT: "observer_thought_id",
}


@base_router.get(
    "/{entity_type}/{entity_id}/artifacts",
    tags=["agent"],
    response_model=list[Artifact],
)
@base_router.get(
    "/{entity_type}/{entity_id}/artifacts/",
    tags=["agent"],
    response_model=list[Artifact],
    include_in_schema=False,
)
async def get_agent_entity_artifacts(
    entity_type: EntityType,
    entity_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Response:
    """
    Get all artifacts for an entity (step, task, workflow_run).

    Args:
        entity_type: Type of entity to fetch artifacts for
        entity_id: ID of the entity
        current_org: Current organization from auth

    Returns:
        List of artifacts for the entity

    Raises:
        HTTPException: If entity is not supported
    """

    if entity_type not in entity_type_to_param:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid entity_type: {entity_type}",
        )

    analytics.capture("skyvern-oss-agent-entity-artifacts-get")

    params = {
        "organization_id": current_org.organization_id,
        entity_type_to_param[entity_type]: entity_id,
    }

    artifacts = await app.DATABASE.get_artifacts_by_entity_id(**params)  # type: ignore

    if settings.ENV != "local" or settings.GENERATE_PRESIGNED_URLS:
        signed_urls = await app.ARTIFACT_MANAGER.get_share_links(artifacts)
        if signed_urls:
            for i, artifact in enumerate(artifacts):
                artifact.signed_url = signed_urls[i]
        else:
            LOG.warning(
                "Failed to get signed urls for artifacts",
                entity_type=entity_type,
                entity_id=entity_id,
            )

    return ORJSONResponse([artifact.model_dump() for artifact in artifacts])


@base_router.get(
    "/tasks/{task_id}/steps/{step_id}/artifacts",
    tags=["agent"],
    response_model=list[Artifact],
)
@base_router.get(
    "/tasks/{task_id}/steps/{step_id}/artifacts/",
    tags=["agent"],
    response_model=list[Artifact],
    include_in_schema=False,
)
async def get_agent_task_step_artifacts(
    task_id: str,
    step_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Response:
    """
    Get all artifacts for a list of steps.
    :param task_id:
    :param step_id:
    :return: List of artifacts for a list of steps.
    """
    analytics.capture("skyvern-oss-agent-task-step-artifacts-get")
    artifacts = await app.DATABASE.get_artifacts_for_task_step(
        task_id,
        step_id,
        organization_id=current_org.organization_id,
    )
    if settings.ENV != "local" or settings.GENERATE_PRESIGNED_URLS:
        signed_urls = await app.ARTIFACT_MANAGER.get_share_links(artifacts)
        if signed_urls:
            for i, artifact in enumerate(artifacts):
                artifact.signed_url = signed_urls[i]
        else:
            LOG.warning(
                "Failed to get signed urls for artifacts",
                task_id=task_id,
                step_id=step_id,
            )
    return ORJSONResponse([artifact.model_dump() for artifact in artifacts])


class ActionResultTmp(BaseModel):
    action: dict[str, Any]
    data: dict[str, Any] | list | str | None = None
    exception_message: str | None = None
    success: bool = True


@base_router.get("/tasks/{task_id}/actions", response_model=list[Action])
@base_router.get(
    "/tasks/{task_id}/actions/",
    response_model=list[Action],
    include_in_schema=False,
)
async def get_task_actions(
    task_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> list[Action]:
    analytics.capture("skyvern-oss-agent-task-actions-get")
    actions = await app.DATABASE.get_task_actions(task_id, organization_id=current_org.organization_id)
    return actions


@base_router.post("/workflows/{workflow_id}/run", response_model=RunWorkflowResponse)
@base_router.post(
    "/workflows/{workflow_id}/run/",
    response_model=RunWorkflowResponse,
    include_in_schema=False,
)
async def execute_workflow(
    request: Request,
    background_tasks: BackgroundTasks,
    workflow_id: str,  # this is the workflow_permanent_id
    workflow_request: WorkflowRequestBody,
    version: int | None = None,
    current_org: Organization = Depends(org_auth_service.get_current_org),
    x_api_key: Annotated[str | None, Header()] = None,
    x_max_steps_override: Annotated[int | None, Header()] = None,
) -> RunWorkflowResponse:
    analytics.capture("skyvern-oss-agent-workflow-execute")
    context = skyvern_context.ensure_context()
    request_id = context.request_id
    workflow_run = await app.WORKFLOW_SERVICE.setup_workflow_run(
        request_id=request_id,
        workflow_request=workflow_request,
        workflow_permanent_id=workflow_id,
        organization_id=current_org.organization_id,
        version=version,
        max_steps_override=x_max_steps_override,
    )
    if x_max_steps_override:
        LOG.info("Overriding max steps per run", max_steps_override=x_max_steps_override)
    await AsyncExecutorFactory.get_executor().execute_workflow(
        request=request,
        background_tasks=background_tasks,
        organization_id=current_org.organization_id,
        workflow_id=workflow_run.workflow_id,
        workflow_run_id=workflow_run.workflow_run_id,
        max_steps_override=x_max_steps_override,
        browser_session_id=workflow_request.browser_session_id,
        api_key=x_api_key,
    )
    return RunWorkflowResponse(
        workflow_id=workflow_id,
        workflow_run_id=workflow_run.workflow_run_id,
    )


@base_router.get(
    "/workflows/runs",
    response_model=list[WorkflowRun],
)
@base_router.get(
    "/workflows/runs/",
    response_model=list[WorkflowRun],
    include_in_schema=False,
)
async def get_workflow_runs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    status: Annotated[list[WorkflowRunStatus] | None, Query()] = None,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> list[WorkflowRun]:
    analytics.capture("skyvern-oss-agent-workflow-runs-get")
    return await app.WORKFLOW_SERVICE.get_workflow_runs(
        organization_id=current_org.organization_id,
        page=page,
        page_size=page_size,
        status=status,
    )


@base_router.get(
    "/workflows/{workflow_permanent_id}/runs",
    response_model=list[WorkflowRun],
)
@base_router.get(
    "/workflows/{workflow_permanent_id}/runs/",
    response_model=list[WorkflowRun],
    include_in_schema=False,
)
async def get_workflow_runs_for_workflow_permanent_id(
    workflow_permanent_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    status: Annotated[list[WorkflowRunStatus] | None, Query()] = None,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> list[WorkflowRun]:
    analytics.capture("skyvern-oss-agent-workflow-runs-get")
    return await app.WORKFLOW_SERVICE.get_workflow_runs_for_workflow_permanent_id(
        workflow_permanent_id=workflow_permanent_id,
        organization_id=current_org.organization_id,
        page=page,
        page_size=page_size,
        status=status,
    )


@base_router.get(
    "/workflows/{workflow_id}/runs/{workflow_run_id}",
)
@base_router.get(
    "/workflows/{workflow_id}/runs/{workflow_run_id}/",
    include_in_schema=False,
)
async def get_workflow_run(
    workflow_id: str,
    workflow_run_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> dict[str, Any]:
    analytics.capture("skyvern-oss-agent-workflow-run-get")
    workflow_run_status_response = await app.WORKFLOW_SERVICE.build_workflow_run_status_response(
        workflow_permanent_id=workflow_id,
        workflow_run_id=workflow_run_id,
        organization_id=current_org.organization_id,
        include_cost=True,
    )
    return_dict = workflow_run_status_response.model_dump()
    observer_cruise = await app.DATABASE.get_observer_cruise_by_workflow_run_id(
        workflow_run_id=workflow_run_id,
        organization_id=current_org.organization_id,
    )
    if observer_cruise:
        return_dict["observer_task"] = observer_cruise.model_dump(by_alias=True)
    return return_dict


@base_router.get(
    "/workflows/{workflow_id}/runs/{workflow_run_id}/timeline",
)
@base_router.get(
    "/workflows/{workflow_id}/runs/{workflow_run_id}/timeline/",
    include_in_schema=False,
)
async def get_workflow_run_timeline(
    workflow_run_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> list[WorkflowRunTimeline]:
    # get observer cruise by workflow run id
    observer_cruise_obj = await app.DATABASE.get_observer_cruise_by_workflow_run_id(
        workflow_run_id=workflow_run_id,
        organization_id=current_org.organization_id,
    )
    # get all the workflow run blocks
    workflow_run_block_timeline = await app.WORKFLOW_SERVICE.get_workflow_run_timeline(
        workflow_run_id=workflow_run_id,
        organization_id=current_org.organization_id,
    )
    if observer_cruise_obj and observer_cruise_obj.observer_cruise_id:
        observer_thought_timeline = await observer_service.get_observer_thought_timelines(
            observer_cruise_id=observer_cruise_obj.observer_cruise_id,
            organization_id=current_org.organization_id,
        )
        workflow_run_block_timeline.extend(observer_thought_timeline)
    workflow_run_block_timeline.sort(key=lambda x: x.created_at, reverse=True)
    return workflow_run_block_timeline


@base_router.get(
    "/workflows/runs/{workflow_run_id}",
    response_model=WorkflowRunStatusResponse,
)
@base_router.get(
    "/workflows/runs/{workflow_run_id}/",
    response_model=WorkflowRunStatusResponse,
    include_in_schema=False,
)
async def get_workflow_run_by_run_id(
    workflow_run_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> WorkflowRunStatusResponse:
    analytics.capture("skyvern-oss-agent-workflow-run-get")
    return await app.WORKFLOW_SERVICE.build_workflow_run_status_response_by_workflow_id(
        workflow_run_id=workflow_run_id,
        organization_id=current_org.organization_id,
    )


@base_router.post(
    "/workflows",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": WorkflowCreateYAMLRequest.model_json_schema()}},
            "required": True,
        },
    },
    response_model=Workflow,
)
@base_router.post(
    "/workflows/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": WorkflowCreateYAMLRequest.model_json_schema()}},
            "required": True,
        },
    },
    response_model=Workflow,
    include_in_schema=False,
)
async def create_workflow(
    request: Request,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Workflow:
    analytics.capture("skyvern-oss-agent-workflow-create")
    raw_yaml = await request.body()
    try:
        workflow_yaml = yaml.safe_load(raw_yaml)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")

    try:
        workflow_create_request = WorkflowCreateYAMLRequest.model_validate(workflow_yaml)
        return await app.WORKFLOW_SERVICE.create_workflow_from_request(
            organization=current_org, request=workflow_create_request
        )
    except WorkflowParameterMissingRequiredValue as e:
        raise e
    except Exception as e:
        LOG.error("Failed to create workflow", exc_info=True, organization_id=current_org.organization_id)
        raise FailedToCreateWorkflow(str(e))


@base_router.put(
    "/workflows/{workflow_permanent_id}",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": WorkflowCreateYAMLRequest.model_json_schema()}},
            "required": True,
        },
    },
    response_model=Workflow,
)
@base_router.put(
    "/workflows/{workflow_permanent_id}/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": WorkflowCreateYAMLRequest.model_json_schema()}},
            "required": True,
        },
    },
    response_model=Workflow,
    include_in_schema=False,
)
async def update_workflow(
    workflow_permanent_id: str,
    request: Request,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Workflow:
    analytics.capture("skyvern-oss-agent-workflow-update")
    # validate the workflow
    raw_yaml = await request.body()
    try:
        workflow_yaml = yaml.safe_load(raw_yaml)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")

    try:
        workflow_create_request = WorkflowCreateYAMLRequest.model_validate(workflow_yaml)
        return await app.WORKFLOW_SERVICE.create_workflow_from_request(
            organization=current_org,
            request=workflow_create_request,
            workflow_permanent_id=workflow_permanent_id,
        )
    except WorkflowParameterMissingRequiredValue as e:
        raise e
    except Exception as e:
        LOG.exception(
            "Failed to update workflow",
            workflow_permanent_id=workflow_permanent_id,
            organization_id=current_org.organization_id,
        )
        raise FailedToUpdateWorkflow(workflow_permanent_id, f"<{type(e).__name__}: {str(e)}>")


@base_router.delete("/workflows/{workflow_permanent_id}")
@base_router.delete("/workflows/{workflow_permanent_id}/", include_in_schema=False)
async def delete_workflow(
    workflow_permanent_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> None:
    analytics.capture("skyvern-oss-agent-workflow-delete")
    await app.WORKFLOW_SERVICE.delete_workflow_by_permanent_id(workflow_permanent_id, current_org.organization_id)


@base_router.get("/workflows", response_model=list[Workflow])
@base_router.get("/workflows/", response_model=list[Workflow])
async def get_workflows(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    only_saved_tasks: bool = Query(False),
    only_workflows: bool = Query(False),
    title: str = Query(""),
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> list[Workflow]:
    """
    Get all workflows with the latest version for the organization.
    """
    analytics.capture("skyvern-oss-agent-workflows-get")

    if only_saved_tasks and only_workflows:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="only_saved_tasks and only_workflows cannot be used together",
        )

    return await app.WORKFLOW_SERVICE.get_workflows_by_organization_id(
        organization_id=current_org.organization_id,
        page=page,
        page_size=page_size,
        only_saved_tasks=only_saved_tasks,
        only_workflows=only_workflows,
        title=title,
    )


@base_router.get("/workflows/{workflow_permanent_id}", response_model=Workflow)
@base_router.get("/workflows/{workflow_permanent_id}/", response_model=Workflow)
async def get_workflow(
    workflow_permanent_id: str,
    version: int | None = None,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Workflow:
    analytics.capture("skyvern-oss-agent-workflows-get")
    return await app.WORKFLOW_SERVICE.get_workflow_by_permanent_id(
        workflow_permanent_id=workflow_permanent_id,
        organization_id=current_org.organization_id,
        version=version,
    )


class AISuggestionType(str, Enum):
    DATA_SCHEMA = "data_schema"


@base_router.post("/suggest/{ai_suggestion_type}", include_in_schema=False)
@base_router.post("/suggest/{ai_suggestion_type}/")
async def make_ai_suggestion(
    ai_suggestion_type: AISuggestionType,
    data: AISuggestionRequest,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> AISuggestionBase:
    llm_prompt = ""

    if ai_suggestion_type == AISuggestionType.DATA_SCHEMA:
        llm_prompt = prompt_engine.load_prompt("suggest-data-schema", input=data.input, additional_context=data.context)

    try:
        new_ai_suggestion = await app.DATABASE.create_ai_suggestion(
            organization_id=current_org.organization_id,
            ai_suggestion_type=ai_suggestion_type,
        )

        llm_response = await app.LLM_API_HANDLER(prompt=llm_prompt, ai_suggestion=new_ai_suggestion)
        parsed_ai_suggestion = AISuggestionBase.model_validate(llm_response)

        return parsed_ai_suggestion

    except LLMProviderError:
        LOG.error("Failed to suggest data schema", exc_info=True)
        raise HTTPException(status_code=400, detail="Failed to suggest data schema. Please try again later.")


@base_router.post("/generate/task", include_in_schema=False)
@base_router.post("/generate/task/")
async def generate_task(
    data: GenerateTaskRequest,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> TaskGeneration:
    user_prompt = data.prompt
    hash_object = hashlib.sha256()
    hash_object.update(user_prompt.encode("utf-8"))
    user_prompt_hash = hash_object.hexdigest()
    # check if there's a same user_prompt within the past x Hours
    # in the future, we can use vector db to fetch similar prompts
    existing_task_generation = await app.DATABASE.get_task_generation_by_prompt_hash(
        user_prompt_hash=user_prompt_hash, query_window_hours=settings.PROMPT_CACHE_WINDOW_HOURS
    )
    if existing_task_generation:
        new_task_generation = await app.DATABASE.create_task_generation(
            organization_id=current_org.organization_id,
            user_prompt=data.prompt,
            user_prompt_hash=user_prompt_hash,
            url=existing_task_generation.url,
            navigation_goal=existing_task_generation.navigation_goal,
            navigation_payload=existing_task_generation.navigation_payload,
            data_extraction_goal=existing_task_generation.data_extraction_goal,
            extracted_information_schema=existing_task_generation.extracted_information_schema,
            llm=existing_task_generation.llm,
            llm_prompt=existing_task_generation.llm_prompt,
            llm_response=existing_task_generation.llm_response,
            source_task_generation_id=existing_task_generation.task_generation_id,
        )
        return new_task_generation

    llm_prompt = prompt_engine.load_prompt("generate-task", user_prompt=data.prompt)
    try:
        llm_response = await app.LLM_API_HANDLER(prompt=llm_prompt)
        parsed_task_generation_obj = TaskGenerationBase.model_validate(llm_response)

        # generate a TaskGenerationModel
        task_generation = await app.DATABASE.create_task_generation(
            organization_id=current_org.organization_id,
            user_prompt=data.prompt,
            user_prompt_hash=user_prompt_hash,
            url=parsed_task_generation_obj.url,
            navigation_goal=parsed_task_generation_obj.navigation_goal,
            navigation_payload=parsed_task_generation_obj.navigation_payload,
            data_extraction_goal=parsed_task_generation_obj.data_extraction_goal,
            extracted_information_schema=parsed_task_generation_obj.extracted_information_schema,
            suggested_title=parsed_task_generation_obj.suggested_title,
            llm=settings.LLM_KEY,
            llm_prompt=llm_prompt,
            llm_response=str(llm_response),
        )
        return task_generation
    except LLMProviderError:
        LOG.error("Failed to generate task", exc_info=True)
        raise HTTPException(status_code=400, detail="Failed to generate task. Please try again later.")
    except OperationalError:
        LOG.error("Database error when generating task", exc_info=True, user_prompt=data.prompt)
        raise HTTPException(status_code=500, detail="Failed to generate task. Please try again later.")


@base_router.put("/organizations/", include_in_schema=False)
@base_router.put("/organizations")
async def update_organization(
    org_update: OrganizationUpdate,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Organization:
    return await app.DATABASE.update_organization(
        current_org.organization_id,
        max_steps_per_run=org_update.max_steps_per_run,
    )


@base_router.get("/organizations/", include_in_schema=False)
@base_router.get("/organizations")
async def get_organizations(
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> GetOrganizationsResponse:
    return GetOrganizationsResponse(organizations=[current_org])


@base_router.get("/organizations/{organization_id}/apikeys/", include_in_schema=False)
@base_router.get("/organizations/{organization_id}/apikeys")
async def get_org_api_keys(
    organization_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> GetOrganizationAPIKeysResponse:
    if organization_id != current_org.organization_id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this organization")
    api_keys = []
    org_auth_token = await app.DATABASE.get_valid_org_auth_token(organization_id, OrganizationAuthTokenType.api)
    if org_auth_token:
        api_keys.append(org_auth_token)
    return GetOrganizationAPIKeysResponse(api_keys=api_keys)


async def validate_file_size(file: UploadFile) -> UploadFile:
    try:
        file.file.seek(0, 2)  # Move the pointer to the end of the file
        size = file.file.tell()  # Get the current position of the pointer, which represents the file size
        file.file.seek(0)  # Reset the pointer back to the beginning
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not determine file size.") from e

    if size > app.SETTINGS_MANAGER.MAX_UPLOAD_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the maximum allowed size ({app.SETTINGS_MANAGER.MAX_UPLOAD_FILE_SIZE / 1024 / 1024} MB)",
        )
    return file


@base_router.post("/upload_file/", include_in_schema=False)
@base_router.post("/upload_file")
async def upload_file(
    file: UploadFile = Depends(validate_file_size),
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> Response:
    bucket = app.SETTINGS_MANAGER.AWS_S3_BUCKET_UPLOADS
    todays_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # First try uploading with original filename
    try:
        sanitized_filename = os.path.basename(file.filename)  # Remove any path components
        s3_uri = (
            f"s3://{bucket}/{app.SETTINGS_MANAGER.ENV}/{current_org.organization_id}/{todays_date}/{sanitized_filename}"
        )
        uploaded_s3_uri = await aws_client.upload_file_stream(s3_uri, file.file)
    except Exception:
        LOG.error("Failed to upload file to S3", exc_info=True)
        uploaded_s3_uri = None

    # If upload fails, try again with UUID prefix
    if not uploaded_s3_uri:
        uuid_prefixed_filename = f"{str(uuid.uuid4())}_{file.filename}"
        s3_uri = f"s3://{bucket}/{app.SETTINGS_MANAGER.ENV}/{current_org.organization_id}/{todays_date}/{uuid_prefixed_filename}"
        file.file.seek(0)  # Reset file pointer
        uploaded_s3_uri = await aws_client.upload_file_stream(s3_uri, file.file)

    if not uploaded_s3_uri:
        raise HTTPException(status_code=500, detail="Failed to upload file to S3.")

    # Generate a presigned URL for the uploaded file
    presigned_urls = await aws_client.create_presigned_urls([uploaded_s3_uri])
    if not presigned_urls:
        raise HTTPException(status_code=500, detail="Failed to generate presigned URL.")

    presigned_url = presigned_urls[0]
    return ORJSONResponse(
        content={"s3_uri": uploaded_s3_uri, "presigned_url": presigned_url},
        status_code=200,
        media_type="application/json",
    )


@v2_router.post("/tasks")
@v2_router.post("/tasks/", include_in_schema=False)
async def observer_task(
    request: Request,
    background_tasks: BackgroundTasks,
    data: ObserverTaskRequest,
    organization: Organization = Depends(org_auth_service.get_current_org),
    x_max_iterations_override: Annotated[int | None, Header()] = None,
) -> dict[str, Any]:
    if x_max_iterations_override:
        LOG.info("Overriding max iterations for observer", max_iterations_override=x_max_iterations_override)

    try:
        observer_task = await observer_service.initialize_observer_cruise(
            organization=organization,
            user_prompt=data.user_prompt,
            user_url=str(data.url) if data.url else None,
            totp_identifier=data.totp_identifier,
            totp_verification_url=data.totp_verification_url,
            webhook_callback_url=data.webhook_callback_url,
            proxy_location=data.proxy_location,
        )
    except LLMProviderError:
        LOG.error("LLM failure to initialize observer cruise", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Skyvern LLM failure to initialize observer cruise. Please try again later."
        )
    analytics.capture("skyvern-oss-agent-observer-cruise", data={"url": observer_task.url})
    await AsyncExecutorFactory.get_executor().execute_cruise(
        request=request,
        background_tasks=background_tasks,
        organization_id=organization.organization_id,
        observer_cruise_id=observer_task.observer_cruise_id,
        max_iterations_override=x_max_iterations_override,
        browser_session_id=data.browser_session_id,
    )
    return observer_task.model_dump(by_alias=True)


@v2_router.get("/tasks/{task_id}")
@v2_router.get("/tasks/{task_id}/", include_in_schema=False)
async def get_observer_task(
    task_id: str,
    organization: Organization = Depends(org_auth_service.get_current_org),
) -> dict[str, Any]:
    observer_task = await observer_service.get_observer_cruise(task_id, organization.organization_id)
    if not observer_task:
        raise HTTPException(status_code=404, detail=f"Observer task {task_id} not found")
    return observer_task.model_dump(by_alias=True)


@base_router.get(
    "/browser_sessions/{browser_session_id}",
    response_model=BrowserSessionResponse,
)
@base_router.get(
    "/browser_sessions/{browser_session_id}/",
    response_model=BrowserSessionResponse,
    include_in_schema=False,
)
async def get_browser_session_by_id(
    browser_session_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> BrowserSessionResponse:
    analytics.capture("skyvern-oss-agent-workflow-run-get")
    browser_session = await app.PERSISTENT_SESSIONS_MANAGER.get_session(
        browser_session_id,
        current_org.organization_id,
    )
    if not browser_session:
        raise HTTPException(status_code=404, detail=f"Browser session {browser_session_id} not found")
    return BrowserSessionResponse.from_browser_session(browser_session)


@base_router.get(
    "/browser_sessions",
    response_model=list[BrowserSessionResponse],
)
@base_router.get(
    "/browser_sessions/",
    response_model=list[BrowserSessionResponse],
    include_in_schema=False,
)
async def get_browser_sessions(
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> list[BrowserSessionResponse]:
    """Get all active browser sessions for the organization"""
    analytics.capture("skyvern-oss-agent-browser-sessions-get")
    browser_sessions = await app.PERSISTENT_SESSIONS_MANAGER.get_active_sessions(current_org.organization_id)
    return [BrowserSessionResponse.from_browser_session(browser_session) for browser_session in browser_sessions]


@base_router.post(
    "/browser_sessions",
    response_model=BrowserSessionResponse,
)
@base_router.post(
    "/browser_sessions/",
    response_model=BrowserSessionResponse,
    include_in_schema=False,
)
async def create_browser_session(
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> BrowserSessionResponse:
    browser_session, _ = await app.PERSISTENT_SESSIONS_MANAGER.create_session(current_org.organization_id)
    return BrowserSessionResponse.from_browser_session(browser_session)


@base_router.post(
    "/browser_sessions/close",
)
@base_router.post(
    "/browser_sessions/close/",
    include_in_schema=False,
)
async def close_browser_sessions(
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> ORJSONResponse:
    await app.PERSISTENT_SESSIONS_MANAGER.close_all_sessions(current_org.organization_id)
    return ORJSONResponse(
        content={"message": "All browser sessions closed"},
        status_code=200,
        media_type="application/json",
    )


@base_router.post(
    "/browser_sessions/{session_id}/close",
)
@base_router.post(
    "/browser_sessions/{session_id}/close/",
    include_in_schema=False,
)
async def close_browser_session(
    session_id: str,
    current_org: Organization = Depends(org_auth_service.get_current_org),
) -> ORJSONResponse:
    await app.PERSISTENT_SESSIONS_MANAGER.close_session(current_org.organization_id, session_id)
    return ORJSONResponse(
        content={"message": "Browser session closed"},
        status_code=200,
        media_type="application/json",
    )
