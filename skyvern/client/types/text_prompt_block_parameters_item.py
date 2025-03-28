# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
import typing
import datetime as dt
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from .value import Value
from .workflow_parameter_type import WorkflowParameterType
from .workflow_parameter_default_value import WorkflowParameterDefaultValue
from ..core.pydantic_utilities import update_forward_refs


class TextPromptBlockParametersItem_AwsSecret(UniversalBaseModel):
    parameter_type: typing.Literal["aws_secret"] = "aws_secret"
    key: str
    description: typing.Optional[str] = None
    aws_secret_parameter_id: str
    workflow_id: str
    aws_key: str
    created_at: dt.datetime
    modified_at: dt.datetime
    deleted_at: typing.Optional[dt.datetime] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class TextPromptBlockParametersItem_BitwardenCreditCardData(UniversalBaseModel):
    parameter_type: typing.Literal["bitwarden_credit_card_data"] = "bitwarden_credit_card_data"
    key: str
    description: typing.Optional[str] = None
    bitwarden_credit_card_data_parameter_id: str
    workflow_id: str
    bitwarden_client_id_aws_secret_key: str
    bitwarden_client_secret_aws_secret_key: str
    bitwarden_master_password_aws_secret_key: str
    bitwarden_collection_id: str
    bitwarden_item_id: str
    created_at: dt.datetime
    modified_at: dt.datetime
    deleted_at: typing.Optional[dt.datetime] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class TextPromptBlockParametersItem_BitwardenLoginCredential(UniversalBaseModel):
    parameter_type: typing.Literal["bitwarden_login_credential"] = "bitwarden_login_credential"
    key: str
    description: typing.Optional[str] = None
    bitwarden_login_credential_parameter_id: str
    workflow_id: str
    bitwarden_client_id_aws_secret_key: str
    bitwarden_client_secret_aws_secret_key: str
    bitwarden_master_password_aws_secret_key: str
    url_parameter_key: typing.Optional[str] = None
    bitwarden_collection_id: typing.Optional[str] = None
    bitwarden_item_id: typing.Optional[str] = None
    created_at: dt.datetime
    modified_at: dt.datetime
    deleted_at: typing.Optional[dt.datetime] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class TextPromptBlockParametersItem_BitwardenSensitiveInformation(UniversalBaseModel):
    parameter_type: typing.Literal["bitwarden_sensitive_information"] = "bitwarden_sensitive_information"
    key: str
    description: typing.Optional[str] = None
    bitwarden_sensitive_information_parameter_id: str
    workflow_id: str
    bitwarden_client_id_aws_secret_key: str
    bitwarden_client_secret_aws_secret_key: str
    bitwarden_master_password_aws_secret_key: str
    bitwarden_collection_id: str
    bitwarden_identity_key: str
    bitwarden_identity_fields: typing.List[str]
    created_at: dt.datetime
    modified_at: dt.datetime
    deleted_at: typing.Optional[dt.datetime] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class TextPromptBlockParametersItem_Context(UniversalBaseModel):
    parameter_type: typing.Literal["context"] = "context"
    key: str
    description: typing.Optional[str] = None
    source: "Source"
    value: typing.Optional[Value] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


from .context_parameter import ContextParameter  # noqa: E402
from .source import Source  # noqa: E402


class TextPromptBlockParametersItem_Credential(UniversalBaseModel):
    parameter_type: typing.Literal["credential"] = "credential"
    key: str
    description: typing.Optional[str] = None
    credential_parameter_id: str
    workflow_id: str
    credential_id: str
    created_at: dt.datetime
    modified_at: dt.datetime
    deleted_at: typing.Optional[dt.datetime] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class TextPromptBlockParametersItem_Output(UniversalBaseModel):
    parameter_type: typing.Literal["output"] = "output"
    key: str
    description: typing.Optional[str] = None
    output_parameter_id: str
    workflow_id: str
    created_at: dt.datetime
    modified_at: dt.datetime
    deleted_at: typing.Optional[dt.datetime] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class TextPromptBlockParametersItem_Workflow(UniversalBaseModel):
    parameter_type: typing.Literal["workflow"] = "workflow"
    key: str
    description: typing.Optional[str] = None
    workflow_parameter_id: str
    workflow_parameter_type: WorkflowParameterType
    workflow_id: str
    default_value: typing.Optional[WorkflowParameterDefaultValue] = None
    created_at: dt.datetime
    modified_at: dt.datetime
    deleted_at: typing.Optional[dt.datetime] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


TextPromptBlockParametersItem = typing.Union[
    TextPromptBlockParametersItem_AwsSecret,
    TextPromptBlockParametersItem_BitwardenCreditCardData,
    TextPromptBlockParametersItem_BitwardenLoginCredential,
    TextPromptBlockParametersItem_BitwardenSensitiveInformation,
    TextPromptBlockParametersItem_Context,
    TextPromptBlockParametersItem_Credential,
    TextPromptBlockParametersItem_Output,
    TextPromptBlockParametersItem_Workflow,
]
update_forward_refs(TextPromptBlockParametersItem_Context)
