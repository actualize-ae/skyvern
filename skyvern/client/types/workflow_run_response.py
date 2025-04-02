# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
from .run_status import RunStatus
import typing
from .output import Output
from .file_info import FileInfo
import datetime as dt
from .workflow_run_request import WorkflowRunRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class WorkflowRunResponse(UniversalBaseModel):
    run_id: str = pydantic.Field()
    """
    Unique identifier for this run
    """

    status: RunStatus = pydantic.Field()
    """
    Current status of the run
    """

    output: typing.Optional[Output] = pydantic.Field(default=None)
    """
    Output data from the run, if any. Format depends on the schema in the input
    """

    downloaded_files: typing.Optional[typing.List[FileInfo]] = pydantic.Field(default=None)
    """
    List of files downloaded during the run
    """

    recording_url: typing.Optional[str] = pydantic.Field(default=None)
    """
    URL to the recording of the run
    """

    failure_reason: typing.Optional[str] = pydantic.Field(default=None)
    """
    Reason for failure if the run failed
    """

    created_at: dt.datetime = pydantic.Field()
    """
    Timestamp when this run was created
    """

    modified_at: dt.datetime = pydantic.Field()
    """
    Timestamp when this run was last modified
    """

    run_request: typing.Optional[WorkflowRunRequest] = pydantic.Field(default=None)
    """
    The original request parameters used to start this workflow run
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
