# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import datetime as dt
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class Organization(UniversalBaseModel):
    organization_id: str
    organization_name: str
    webhook_callback_url: typing.Optional[str] = None
    max_steps_per_run: typing.Optional[int] = None
    max_retries_per_step: typing.Optional[int] = None
    domain: typing.Optional[str] = None
    bw_organization_id: typing.Optional[str] = None
    bw_collection_ids: typing.Optional[typing.List[str]] = None
    created_at: dt.datetime
    modified_at: dt.datetime

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
