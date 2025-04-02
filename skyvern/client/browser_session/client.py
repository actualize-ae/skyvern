# This file was auto-generated by Fern from our API Definition.

from ..core.client_wrapper import SyncClientWrapper
import typing
from ..core.request_options import RequestOptions
from ..types.browser_session_response import BrowserSessionResponse
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import parse_obj_as
from ..errors.unauthorized_error import UnauthorizedError
from ..errors.not_found_error import NotFoundError
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper


class BrowserSessionClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get_browser_session(
        self, browser_session_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> BrowserSessionResponse:
        """
        Get details about a specific browser session by ID

        Parameters
        ----------
        browser_session_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BrowserSessionResponse
            Successfully retrieved browser session details

        Examples
        --------
        from skyvern import Skyvern

        client = Skyvern(
            api_key="YOUR_API_KEY",
            authorization="YOUR_AUTHORIZATION",
        )
        client.browser_session.get_browser_session(
            browser_session_id="browser_session_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/browser_sessions/{jsonable_encoder(browser_session_id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    BrowserSessionResponse,
                    parse_obj_as(
                        type_=BrowserSessionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_browser_sessions(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[BrowserSessionResponse]:
        """
        Get all active browser sessions for the organization

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[BrowserSessionResponse]
            Successfully retrieved all active browser sessions

        Examples
        --------
        from skyvern import Skyvern

        client = Skyvern(
            api_key="YOUR_API_KEY",
            authorization="YOUR_AUTHORIZATION",
        )
        client.browser_session.get_browser_sessions()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/browser_sessions",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[BrowserSessionResponse],
                    parse_obj_as(
                        type_=typing.List[BrowserSessionResponse],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_browser_session(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> BrowserSessionResponse:
        """
        Create a new browser session

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BrowserSessionResponse
            Successfully created browser session

        Examples
        --------
        from skyvern import Skyvern

        client = Skyvern(
            api_key="YOUR_API_KEY",
            authorization="YOUR_AUTHORIZATION",
        )
        client.browser_session.create_browser_session()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/browser_sessions",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    BrowserSessionResponse,
                    parse_obj_as(
                        type_=BrowserSessionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def close_browser_session(
        self, browser_session_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Optional[typing.Any]:
        """
        Close a browser session

        Parameters
        ----------
        browser_session_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successfully closed browser session

        Examples
        --------
        from skyvern import Skyvern

        client = Skyvern(
            api_key="YOUR_API_KEY",
            authorization="YOUR_AUTHORIZATION",
        )
        client.browser_session.close_browser_session(
            browser_session_id="browser_session_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/browser_sessions/{jsonable_encoder(browser_session_id)}/close",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    parse_obj_as(
                        type_=typing.Optional[typing.Any],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncBrowserSessionClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get_browser_session(
        self, browser_session_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> BrowserSessionResponse:
        """
        Get details about a specific browser session by ID

        Parameters
        ----------
        browser_session_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BrowserSessionResponse
            Successfully retrieved browser session details

        Examples
        --------
        import asyncio

        from skyvern import AsyncSkyvern

        client = AsyncSkyvern(
            api_key="YOUR_API_KEY",
            authorization="YOUR_AUTHORIZATION",
        )


        async def main() -> None:
            await client.browser_session.get_browser_session(
                browser_session_id="browser_session_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/browser_sessions/{jsonable_encoder(browser_session_id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    BrowserSessionResponse,
                    parse_obj_as(
                        type_=BrowserSessionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_browser_sessions(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[BrowserSessionResponse]:
        """
        Get all active browser sessions for the organization

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[BrowserSessionResponse]
            Successfully retrieved all active browser sessions

        Examples
        --------
        import asyncio

        from skyvern import AsyncSkyvern

        client = AsyncSkyvern(
            api_key="YOUR_API_KEY",
            authorization="YOUR_AUTHORIZATION",
        )


        async def main() -> None:
            await client.browser_session.get_browser_sessions()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/browser_sessions",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[BrowserSessionResponse],
                    parse_obj_as(
                        type_=typing.List[BrowserSessionResponse],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_browser_session(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> BrowserSessionResponse:
        """
        Create a new browser session

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BrowserSessionResponse
            Successfully created browser session

        Examples
        --------
        import asyncio

        from skyvern import AsyncSkyvern

        client = AsyncSkyvern(
            api_key="YOUR_API_KEY",
            authorization="YOUR_AUTHORIZATION",
        )


        async def main() -> None:
            await client.browser_session.create_browser_session()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/browser_sessions",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    BrowserSessionResponse,
                    parse_obj_as(
                        type_=BrowserSessionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def close_browser_session(
        self, browser_session_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Optional[typing.Any]:
        """
        Close a browser session

        Parameters
        ----------
        browser_session_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successfully closed browser session

        Examples
        --------
        import asyncio

        from skyvern import AsyncSkyvern

        client = AsyncSkyvern(
            api_key="YOUR_API_KEY",
            authorization="YOUR_AUTHORIZATION",
        )


        async def main() -> None:
            await client.browser_session.close_browser_session(
                browser_session_id="browser_session_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/browser_sessions/{jsonable_encoder(browser_session_id)}/close",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    parse_obj_as(
                        type_=typing.Optional[typing.Any],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
