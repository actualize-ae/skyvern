# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class FileInfo(UniversalBaseModel):
    """
    Information about a downloaded file, including URL and checksum.
    """

    url: str = pydantic.Field()
    """
    URL to access the file
    """

    checksum: typing.Optional[str] = pydantic.Field(default=None)
    """
    SHA-256 checksum of the file
    """

    filename: typing.Optional[str] = pydantic.Field(default=None)
    """
    Original filename
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
