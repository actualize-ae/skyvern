# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
from .context_parameter import ContextParameter
import typing
from .output_parameter import OutputParameter
from .action_block_data_schema import ActionBlockDataSchema
from .action_block_parameters_item import ActionBlockParametersItem
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from .code_block_parameters_item import CodeBlockParametersItem
from .extraction_block_data_schema import ExtractionBlockDataSchema
from .extraction_block_parameters_item import ExtractionBlockParametersItem
from .file_download_block_data_schema import FileDownloadBlockDataSchema
from .file_download_block_parameters_item import FileDownloadBlockParametersItem
from .file_type import FileType
from .for_loop_block_loop_over import ForLoopBlockLoopOver
from .url_block_data_schema import UrlBlockDataSchema
from .url_block_parameters_item import UrlBlockParametersItem
from .login_block_data_schema import LoginBlockDataSchema
from .login_block_parameters_item import LoginBlockParametersItem
from .navigation_block_data_schema import NavigationBlockDataSchema
from .navigation_block_parameters_item import NavigationBlockParametersItem
from .aws_secret_parameter import AwsSecretParameter
from .task_block_data_schema import TaskBlockDataSchema
from .task_block_parameters_item import TaskBlockParametersItem
from .text_prompt_block_parameters_item import TextPromptBlockParametersItem
from .validation_block_data_schema import ValidationBlockDataSchema
from .validation_block_parameters_item import ValidationBlockParametersItem
from .wait_block_parameters_item import WaitBlockParametersItem
from ..core.pydantic_utilities import update_forward_refs


class WorkflowDefinitionBlocksItem_Action(UniversalBaseModel):
    block_type: typing.Literal["action"] = "action"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    task_type: typing.Optional[str] = None
    url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    complete_criterion: typing.Optional[str] = None
    terminate_criterion: typing.Optional[str] = None
    navigation_goal: typing.Optional[str] = None
    data_extraction_goal: typing.Optional[str] = None
    data_schema: typing.Optional[ActionBlockDataSchema] = None
    error_code_mapping: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    max_retries: typing.Optional[int] = None
    max_steps_per_run: typing.Optional[int] = None
    parameters: typing.Optional[typing.List[ActionBlockParametersItem]] = None
    complete_on_download: typing.Optional[bool] = None
    download_suffix: typing.Optional[str] = None
    totp_verification_url: typing.Optional[str] = None
    totp_identifier: typing.Optional[str] = None
    cache_actions: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_Code(UniversalBaseModel):
    block_type: typing.Literal["code"] = "code"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    code: str
    parameters: typing.Optional[typing.List[CodeBlockParametersItem]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_DownloadToS3(UniversalBaseModel):
    block_type: typing.Literal["download_to_s3"] = "download_to_s3"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    url: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_Extraction(UniversalBaseModel):
    block_type: typing.Literal["extraction"] = "extraction"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    task_type: typing.Optional[str] = None
    url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    complete_criterion: typing.Optional[str] = None
    terminate_criterion: typing.Optional[str] = None
    navigation_goal: typing.Optional[str] = None
    data_extraction_goal: str
    data_schema: typing.Optional[ExtractionBlockDataSchema] = None
    error_code_mapping: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    max_retries: typing.Optional[int] = None
    max_steps_per_run: typing.Optional[int] = None
    parameters: typing.Optional[typing.List[ExtractionBlockParametersItem]] = None
    complete_on_download: typing.Optional[bool] = None
    download_suffix: typing.Optional[str] = None
    totp_verification_url: typing.Optional[str] = None
    totp_identifier: typing.Optional[str] = None
    cache_actions: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_FileDownload(UniversalBaseModel):
    block_type: typing.Literal["file_download"] = "file_download"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    task_type: typing.Optional[str] = None
    url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    complete_criterion: typing.Optional[str] = None
    terminate_criterion: typing.Optional[str] = None
    navigation_goal: typing.Optional[str] = None
    data_extraction_goal: typing.Optional[str] = None
    data_schema: typing.Optional[FileDownloadBlockDataSchema] = None
    error_code_mapping: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    max_retries: typing.Optional[int] = None
    max_steps_per_run: typing.Optional[int] = None
    parameters: typing.Optional[typing.List[FileDownloadBlockParametersItem]] = None
    complete_on_download: typing.Optional[bool] = None
    download_suffix: typing.Optional[str] = None
    totp_verification_url: typing.Optional[str] = None
    totp_identifier: typing.Optional[str] = None
    cache_actions: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_FileUrlParser(UniversalBaseModel):
    block_type: typing.Literal["file_url_parser"] = "file_url_parser"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    file_url: str
    file_type: FileType = "csv"

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_ForLoop(UniversalBaseModel):
    block_type: typing.Literal["for_loop"] = "for_loop"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    loop_blocks: typing.List["ForLoopBlockLoopBlocksItem"]
    loop_over: typing.Optional[ForLoopBlockLoopOver] = None
    loop_variable_reference: typing.Optional[str] = None
    complete_if_empty: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


from .for_loop_block import ForLoopBlock  # noqa: E402
from .for_loop_block_loop_blocks_item import ForLoopBlockLoopBlocksItem  # noqa: E402


class WorkflowDefinitionBlocksItem_GotoUrl(UniversalBaseModel):
    block_type: typing.Literal["goto_url"] = "goto_url"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    task_type: typing.Optional[str] = None
    url: str
    title: typing.Optional[str] = None
    complete_criterion: typing.Optional[str] = None
    terminate_criterion: typing.Optional[str] = None
    navigation_goal: typing.Optional[str] = None
    data_extraction_goal: typing.Optional[str] = None
    data_schema: typing.Optional[UrlBlockDataSchema] = None
    error_code_mapping: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    max_retries: typing.Optional[int] = None
    max_steps_per_run: typing.Optional[int] = None
    parameters: typing.Optional[typing.List[UrlBlockParametersItem]] = None
    complete_on_download: typing.Optional[bool] = None
    download_suffix: typing.Optional[str] = None
    totp_verification_url: typing.Optional[str] = None
    totp_identifier: typing.Optional[str] = None
    cache_actions: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_Login(UniversalBaseModel):
    block_type: typing.Literal["login"] = "login"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    task_type: typing.Optional[str] = None
    url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    complete_criterion: typing.Optional[str] = None
    terminate_criterion: typing.Optional[str] = None
    navigation_goal: typing.Optional[str] = None
    data_extraction_goal: typing.Optional[str] = None
    data_schema: typing.Optional[LoginBlockDataSchema] = None
    error_code_mapping: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    max_retries: typing.Optional[int] = None
    max_steps_per_run: typing.Optional[int] = None
    parameters: typing.Optional[typing.List[LoginBlockParametersItem]] = None
    complete_on_download: typing.Optional[bool] = None
    download_suffix: typing.Optional[str] = None
    totp_verification_url: typing.Optional[str] = None
    totp_identifier: typing.Optional[str] = None
    cache_actions: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_Navigation(UniversalBaseModel):
    block_type: typing.Literal["navigation"] = "navigation"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    task_type: typing.Optional[str] = None
    url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    complete_criterion: typing.Optional[str] = None
    terminate_criterion: typing.Optional[str] = None
    navigation_goal: str
    data_extraction_goal: typing.Optional[str] = None
    data_schema: typing.Optional[NavigationBlockDataSchema] = None
    error_code_mapping: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    max_retries: typing.Optional[int] = None
    max_steps_per_run: typing.Optional[int] = None
    parameters: typing.Optional[typing.List[NavigationBlockParametersItem]] = None
    complete_on_download: typing.Optional[bool] = None
    download_suffix: typing.Optional[str] = None
    totp_verification_url: typing.Optional[str] = None
    totp_identifier: typing.Optional[str] = None
    cache_actions: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_PdfParser(UniversalBaseModel):
    block_type: typing.Literal["pdf_parser"] = "pdf_parser"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    file_url: str
    json_schema: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_SendEmail(UniversalBaseModel):
    block_type: typing.Literal["send_email"] = "send_email"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    smtp_host: AwsSecretParameter
    smtp_port: AwsSecretParameter
    smtp_username: AwsSecretParameter
    smtp_password: AwsSecretParameter
    sender: str
    recipients: typing.List[str]
    subject: str
    body: str
    file_attachments: typing.Optional[typing.List[str]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_Task(UniversalBaseModel):
    block_type: typing.Literal["task"] = "task"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    task_type: typing.Optional[str] = None
    url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    complete_criterion: typing.Optional[str] = None
    terminate_criterion: typing.Optional[str] = None
    navigation_goal: typing.Optional[str] = None
    data_extraction_goal: typing.Optional[str] = None
    data_schema: typing.Optional[TaskBlockDataSchema] = None
    error_code_mapping: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    max_retries: typing.Optional[int] = None
    max_steps_per_run: typing.Optional[int] = None
    parameters: typing.Optional[typing.List[TaskBlockParametersItem]] = None
    complete_on_download: typing.Optional[bool] = None
    download_suffix: typing.Optional[str] = None
    totp_verification_url: typing.Optional[str] = None
    totp_identifier: typing.Optional[str] = None
    cache_actions: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_TaskV2(UniversalBaseModel):
    block_type: typing.Literal["task_v2"] = "task_v2"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    prompt: str
    url: typing.Optional[str] = None
    totp_verification_url: typing.Optional[str] = None
    totp_identifier: typing.Optional[str] = None
    max_iterations: typing.Optional[int] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_TextPrompt(UniversalBaseModel):
    block_type: typing.Literal["text_prompt"] = "text_prompt"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    llm_key: typing.Optional[str] = None
    prompt: str
    parameters: typing.Optional[typing.List[TextPromptBlockParametersItem]] = None
    json_schema: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_UploadToS3(UniversalBaseModel):
    block_type: typing.Literal["upload_to_s3"] = "upload_to_s3"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    path: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_Validation(UniversalBaseModel):
    block_type: typing.Literal["validation"] = "validation"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    task_type: typing.Optional[str] = None
    url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    complete_criterion: typing.Optional[str] = None
    terminate_criterion: typing.Optional[str] = None
    navigation_goal: typing.Optional[str] = None
    data_extraction_goal: typing.Optional[str] = None
    data_schema: typing.Optional[ValidationBlockDataSchema] = None
    error_code_mapping: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    max_retries: typing.Optional[int] = None
    max_steps_per_run: typing.Optional[int] = None
    parameters: typing.Optional[typing.List[ValidationBlockParametersItem]] = None
    complete_on_download: typing.Optional[bool] = None
    download_suffix: typing.Optional[str] = None
    totp_verification_url: typing.Optional[str] = None
    totp_identifier: typing.Optional[str] = None
    cache_actions: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class WorkflowDefinitionBlocksItem_Wait(UniversalBaseModel):
    block_type: typing.Literal["wait"] = "wait"
    label: str
    output_parameter: OutputParameter
    continue_on_failure: typing.Optional[bool] = None
    wait_sec: int
    parameters: typing.Optional[typing.List[WaitBlockParametersItem]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


WorkflowDefinitionBlocksItem = typing.Union[
    WorkflowDefinitionBlocksItem_Action,
    WorkflowDefinitionBlocksItem_Code,
    WorkflowDefinitionBlocksItem_DownloadToS3,
    WorkflowDefinitionBlocksItem_Extraction,
    WorkflowDefinitionBlocksItem_FileDownload,
    WorkflowDefinitionBlocksItem_FileUrlParser,
    WorkflowDefinitionBlocksItem_ForLoop,
    WorkflowDefinitionBlocksItem_GotoUrl,
    WorkflowDefinitionBlocksItem_Login,
    WorkflowDefinitionBlocksItem_Navigation,
    WorkflowDefinitionBlocksItem_PdfParser,
    WorkflowDefinitionBlocksItem_SendEmail,
    WorkflowDefinitionBlocksItem_Task,
    WorkflowDefinitionBlocksItem_TaskV2,
    WorkflowDefinitionBlocksItem_TextPrompt,
    WorkflowDefinitionBlocksItem_UploadToS3,
    WorkflowDefinitionBlocksItem_Validation,
    WorkflowDefinitionBlocksItem_Wait,
]
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_Action=WorkflowDefinitionBlocksItem_Action)
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_Code=WorkflowDefinitionBlocksItem_Code)
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_Extraction=WorkflowDefinitionBlocksItem_Extraction)
update_forward_refs(
    ContextParameter, WorkflowDefinitionBlocksItem_FileDownload=WorkflowDefinitionBlocksItem_FileDownload
)
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_ForLoop=WorkflowDefinitionBlocksItem_ForLoop)
update_forward_refs(ForLoopBlock, WorkflowDefinitionBlocksItem_ForLoop=WorkflowDefinitionBlocksItem_ForLoop)
update_forward_refs(WorkflowDefinitionBlocksItem_ForLoop)
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_GotoUrl=WorkflowDefinitionBlocksItem_GotoUrl)
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_Login=WorkflowDefinitionBlocksItem_Login)
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_Navigation=WorkflowDefinitionBlocksItem_Navigation)
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_Task=WorkflowDefinitionBlocksItem_Task)
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_TextPrompt=WorkflowDefinitionBlocksItem_TextPrompt)
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_Validation=WorkflowDefinitionBlocksItem_Validation)
update_forward_refs(ContextParameter, WorkflowDefinitionBlocksItem_Wait=WorkflowDefinitionBlocksItem_Wait)
