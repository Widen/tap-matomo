"""REST client handling, including matomoStream base class."""

from __future__ import annotations
import logging
import decimal
import sys
import typing as t
from importlib import resources
import requests


from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class matomoStream(RESTStream):
    """matomo stream class."""

    # Update this value if necessary or override `parse_response`.
    records_jsonpath = "$[*]"

    # Update this value if necessary or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

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

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance, or ``None`` to indicate pagination
            is not supported.
        """
        return super().get_new_paginator()

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
        if next_page_token:
            params["page"] = next_page_token
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


