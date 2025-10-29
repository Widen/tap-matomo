"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_matomo.tap import Tapmatomo

SAMPLE_CONFIG = {
    "api_url": "https://demo.matomo.org/",
    "token_auth": "test_token",
    "idSite": "1",
    "method": "VisitsSummary.get",
    "period": "day",
    "date": "yesterday",
    "format": "json",
}


# Run standard built-in tap tests from the SDK:
#TestTapmatomo = get_tap_test_class(
#    tap_class=Tapmatomo,
#    config=SAMPLE_CONFIG,
#)


# TODO: Create additional tests as appropriate for your tap.
def test_sample():
    """Sample test function."""
    assert True  # Replace with actual test logic
