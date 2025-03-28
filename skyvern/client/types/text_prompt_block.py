# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .context_parameter import ContextParameter
from .output_parameter import OutputParameter
import typing
from .text_prompt_block_parameters_item import TextPromptBlockParametersItem
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class TextPromptBlock(UniversalBaseModel):
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
