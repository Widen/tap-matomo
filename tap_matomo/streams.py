"""Stream type classes for tap-matomo."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_matomo.client import matomoStream

class VisitsDetails(matomoStream):
    """Define custom stream."""

    name = "VisitsDetails"
    path = ""
    primary_keys: t.ClassVar[list[str]] = ["idSite","idVisit"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("idSite", th.IntegerType),
        th.Property("idVisit", th.IntegerType),
        th.Property("visitIp", th.StringType),
        th.Property("visitorId", th.StringType),
        th.Property("fingerprint", th.StringType),
        th.Property(
            "actionDetails",
            th.ArrayType(
                th.ObjectType(
                    th.Property("type", th.StringType),
                    th.Property("url", th.StringType),
                    th.Property("pageTitle", th.StringType),
                    th.Property("pageIdAction", th.IntegerType),
                    th.Property("idpageview", th.StringType),
                    th.Property("serverTimePretty", th.StringType),
                    th.Property("pageId", th.IntegerType),
                    th.Property("pageLoadTime", th.StringType),
                    th.Property("timeSpent", th.IntegerType),
                    th.Property("timeSpentPretty", th.StringType),
                    th.Property("pageLoadTimeMilliseconds", th.IntegerType),
                    th.Property("pageviewPosition", th.IntegerType),
                    th.Property("title", th.StringType),
                    th.Property("subtitle", th.StringType),
                    th.Property("icon", th.StringType),
                    th.Property("iconSVG", th.StringType),
                    th.Property("timestamp", th.IntegerType),
                )
            ),
        ),
        th.Property("goalConversions", th.IntegerType),
        th.Property("siteCurrency", th.StringType),
        th.Property("siteCurrencySymbol", th.StringType),
        th.Property("serverDate", th.StringType),
        th.Property("visitServerHour", th.StringType),
        th.Property("lastActionTimestamp", th.IntegerType),
        th.Property("lastActionDateTime", th.StringType),
        th.Property("siteName", th.StringType),
        th.Property("serverTimestamp", th.IntegerType),
        th.Property("firstActionTimestamp", th.IntegerType),
        th.Property("serverTimePretty", th.StringType),
        th.Property("serverDatePretty", th.StringType),
        th.Property("serverDatePrettyFirstAction", th.StringType),
        th.Property("serverTimePrettyFirstAction", th.StringType),
        th.Property("userId", th.StringType),
        th.Property("visitorType", th.StringType),
        th.Property("visitorTypeIcon", th.StringType),
        th.Property("visitConverted", th.IntegerType),
        th.Property("visitConvertedIcon", th.StringType),
        th.Property("visitCount", th.IntegerType),
        th.Property("visitEcommerceStatus", th.StringType),
        th.Property("visitEcommerceStatusIcon", th.StringType),
        th.Property("daysSinceFirstVisit", th.IntegerType),
        th.Property("secondsSinceFirstVisit", th.IntegerType),
        th.Property("daysSinceLastEcommerceOrder", th.IntegerType),
        th.Property("secondsSinceLastEcommerceOrder", th.IntegerType),
        th.Property("visitDuration", th.IntegerType),
        th.Property("visitDurationPretty", th.StringType),
        th.Property("searches", th.IntegerType),
        th.Property("actions", th.IntegerType),
        th.Property("interactions", th.IntegerType),
        th.Property("referrerType", th.StringType),
        th.Property("referrerTypeName", th.StringType),
        th.Property("referrerName", th.StringType),
        th.Property("referrerKeyword", th.StringType),
        th.Property("referrerKeywordPosition", th.StringType),
        th.Property("referrerUrl", th.StringType),
        th.Property("referrerSearchEngineUrl", th.StringType),
        th.Property("referrerSearchEngineIcon", th.StringType),
        th.Property("referrerSocialNetworkUrl", th.StringType),
        th.Property("referrerSocialNetworkIcon", th.StringType),
        th.Property("languageCode", th.StringType),
        th.Property("language", th.StringType),
        th.Property("deviceType", th.StringType),
        th.Property("deviceTypeIcon", th.StringType),
        th.Property("deviceBrand", th.StringType),
        th.Property("deviceModel", th.StringType),
        th.Property("operatingSystem", th.StringType),
        th.Property("operatingSystemName", th.StringType),
        th.Property("operatingSystemIcon", th.StringType),
        th.Property("operatingSystemCode", th.StringType),
        th.Property("operatingSystemVersion", th.StringType),
        th.Property("browserFamily", th.StringType),
        th.Property("browserFamilyDescription", th.StringType),
        th.Property("browser", th.StringType),
        th.Property("browserName", th.StringType),
        th.Property("browserIcon", th.StringType),
        th.Property("browserCode", th.StringType),
        th.Property("browserVersion", th.StringType),
        th.Property("events", th.IntegerType),
        th.Property("continent", th.StringType),
        th.Property("continentCode", th.StringType),
        th.Property("country", th.StringType),
        th.Property("countryCode", th.StringType),
        th.Property("countryFlag", th.StringType),
        th.Property("region", th.StringType),
        th.Property("regionCode", th.StringType),
        th.Property("city", th.StringType),
        th.Property("location", th.StringType),
        th.Property("latitude", th.StringType),
        th.Property("longitude", th.StringType),
        th.Property("visitLocalTime", th.StringType),
        th.Property("visitLocalHour", th.StringType),
        th.Property("daysSinceLastVisit", th.IntegerType),
        th.Property("secondsSinceLastVisit", th.IntegerType),
        th.Property("resolution", th.StringType),
        th.Property("plugins", th.StringType),
        th.Property(
            "pluginsIcons",
            th.ArrayType(
                th.ObjectType(
                    th.Property("pluginIcon", th.StringType),
                    th.Property("pluginName", th.StringType),
                )
            ),
        ),
        th.Property("dimension1", th.StringType),
        th.Property("dimension2", th.StringType),
        th.Property("provider", th.StringType),
        th.Property("providerName", th.StringType),
        th.Property("providerUrl", th.StringType),
        th.Property("truncatedActionsCount", th.IntegerType)
    ).to_dict()




