# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .output_parameter import OutputParameter
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class UploadToS3Block(UniversalBaseModel):
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
