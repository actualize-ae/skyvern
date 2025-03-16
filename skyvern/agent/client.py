from enum import StrEnum

import httpx

from skyvern.config import settings
from skyvern.exceptions import SkyvernClientException
from skyvern.forge.sdk.schemas.task_runs import TaskRunResponse
from skyvern.forge.sdk.schemas.tasks import ProxyLocation
from skyvern.forge.sdk.workflow.models.workflow import WorkflowRunStatusResponse


class RunEngine(StrEnum):
    skyvern_v1 = "skyvern-1.0"
    skyvern_v2 = "skyvern-2.0"


class SkyvernClient:
    def __init__(
        self,
        base_url: str = settings.SKYVERN_BASE_URL,
        api_key: str = settings.SKYVERN_API_KEY,
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key

    async def run_task(
        self,
        goal: str,
        engine: RunEngine = RunEngine.skyvern_v1,
        url: str | None = None,
        webhook_url: str | None = None,
        totp_identifier: str | None = None,
        totp_url: str | None = None,
        title: str | None = None,
        error_code_mapping: dict[str, str] | None = None,
        proxy_location: ProxyLocation | None = None,
        max_steps: int | None = None,
    ) -> TaskRunResponse:
        if engine == RunEngine.skyvern_v1:
            return TaskRunResponse()
        elif engine == RunEngine.skyvern_v2:
            return TaskRunResponse()
        raise ValueError(f"Invalid engine: {engine}")

    async def run_workflow(
        self,
        workflow_id: str,
        webhook_url: str | None = None,
        proxy_location: ProxyLocation | None = None,
    ) -> TaskRunResponse:
        return TaskRunResponse()

    async def get_run(
        self,
        run_id: str,
    ) -> TaskRunResponse:
        return TaskRunResponse()

    async def get_workflow_run(
        self,
        workflow_run_id: str,
    ) -> WorkflowRunStatusResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/workflows/runs/{workflow_run_id}",
                headers={"x-api-key": self.api_key},
            )
            if response.status_code != 200:
                raise SkyvernClientException(
                    f"Failed to get workflow run: {response.text}",
                    status_code=response.status_code,
                )
            return WorkflowRunStatusResponse.model_validate(response.json())
