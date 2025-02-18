# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .organization_auth_token_type import OrganizationAuthTokenType
import datetime as dt
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class OrganizationAuthToken(UniversalBaseModel):
    id: str
    organization_id: str
    token_type: OrganizationAuthTokenType = "api"
    token: str
    valid: bool
    created_at: dt.datetime
    modified_at: dt.datetime

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
