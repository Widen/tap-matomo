"""matomo tap class."""

from __future__ import annotations

import sys

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_matomo import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

class Tapmatomo(Tap):
    """matomo tap class."""

    name = "tap-matomo"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="Auth Token",
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "idSite",
            th.StringType(nullable=False),
            required=True,
            title="idSite",
            description="The integer id of your website,you can also specify a list of idSites comma separated, eg. idSite=1,4,5,6",
        ),
        th.Property(
            "method",
            th.StringType(nullable=False),
            required=True,
            default="Live.getLastVisitsDetails",
            title="method",
            description="The API method you want to call.",
        ),
        th.Property(
            "period",
            th.StringType(nullable=False),
            required=True,
            default="day",
            title="period",
            description="The period you request the statistics for. Can be any of: day, week, month, year or range. All reports are returned for the dates based on the website's time zone.",
        ),
        th.Property(
            "date",
            th.DateTimeType(nullable=True),
            description="standard format = YYYY-MM-DD or magic keywords = today, yesterday, lastWeek, lastMonth or lastYear. These are relative the website timezone. ",
        ),
        th.Property(
            "api_url",
            th.StringType(nullable=False),
            title="API URL",
            description="The url for the API service",
        ),
        th.Property(
            "format",
            th.StringType(nullable=False),
            default='json',
            title="format",
            description="Defines the format of the output.",
        ),
        th.Property(
            "filter_limit",
            th.StringType(nullable=False),
            default='1000',
            title="filter_limit",
            description="Defines the format of the output.",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[streams.matomoStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.VisitsDetails(self),
        ]


if __name__ == "__main__":
    Tapmatomo.cli()
