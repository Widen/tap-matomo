"""REST client handling, including matomoStream base class."""

from __future__ import annotations
import logging
import decimal
import sys
import typing as t
from importlib import resources
import requests


from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, BasePageNumberPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context

class MatomoOffsetPaginator(BasePageNumberPaginator):
    """Paginator for Matomo API using filter_offset."""

    def __init__(self, start_value: int, page_size: int, *args, **kwargs) -> None:
        """Initialize paginator.

        Args:
            start_value: Initial offset value.
            page_size: Number of records per page (filter_limit).
        """
        super().__init__(start_value, *args, **kwargs)
        self._page_size = int(page_size)
        self._has_more = True
        self._pagination_disabled = int(page_size) == -1
        if self._pagination_disabled:
            logging.info("Pagination disabled (filter_limit=-1)")

    @override
    def has_more(self, response: requests.Response) -> bool:
        """Check if there are more pages.

        Args:
            response: HTTP response object.

        Returns:
            True if there are more pages to fetch.
        """
        if self._pagination_disabled:
            return False
        data = response.json()

        return bool(data)

    @override
    def get_next(self, response: requests.Response) -> int | None:
        """Get the next offset value.

        Args:
            response: HTTP response object.

        Returns:
            Next offset value or None if no more pages.
        """
        if self._pagination_disabled or not self.has_more(response):
            return None
        current = int(self.current_value) if isinstance(self.current_value, str) else self.current_value
        return current + self._page_size


class matomoStream(RESTStream):
    """matomo stream class."""
    records_jsonpath = "$[*]"

    @override
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get("api_url","")  # noqa: ERA001

    @property
    @override
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    @override
    def get_new_paginator(self) -> BaseAPIPaginator | None:
        """Create a new pagination helper instance.

        Returns:
            A pagination helper instance for offset-based pagination.
        """
        return MatomoOffsetPaginator(
            start_value=0,
            page_size=self.config.get("filter_limit", 100)
        )

    @property
    def request_method(self) -> str:
        return "POST"

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        params: dict = {}
        params = {
            "module":"API",
            "method": self.config.get("method"),
            "idSite": self.config.get("idSite"),
            "period": self.config.get("period"),
            "date": self.config.get("date"),
            "format": self.config.get("format"),
            "filter_limit": self.config.get("filter_limit"),

        }
        # Add filter_offset for pagination
        if next_page_token is not None:
            params["filter_offset"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    @override
    def prepare_request_payload(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict | None:
        data = {"token_auth": self.config.get("token_auth")}
        return data

    @override
    def prepare_request(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> requests.PreparedRequest:
        """Prepare the request."""


        http_method = self.request_method
        url = self.get_url(context)
        params = self.get_url_params(context, next_page_token)
        headers = self.http_headers
        payload = self.prepare_request_payload(context, next_page_token)

        return requests.Request(
            method=http_method,
            url=url,
            params=params,
            headers=headers,
            data=payload
        ).prepare()

    @override
    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )
    @override
    def validate_response(self, response: requests.Response) -> None:
        """Validate response and raise exception if error found.

        Args:
            response: HTTP response object.

        Raises:
            Exception: If response contains an error.
        """
        super().validate_response(response)

        try:
            data = response.json()
            # Check if response contains an error
            if isinstance(data, dict) and "result" in data and data["result"] == "error":
                error_message = data.get("message", "Unknown error occurred")
                logging.error(f"Matomo API Error: {error_message}")
                raise Exception(f"Matomo API Error: {error_message}")
        except ValueError:
            # Response is not JSON, let parent class handle it
            pass

