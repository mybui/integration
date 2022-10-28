import datetime
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from dateutil.tz import tzutc
from hubspot.crm.companies.models.collection_response_with_total_simple_public_object_forward_paging import (
    CollectionResponseWithTotalSimplePublicObjectForwardPaging,
)
from hubspot.crm.companies.models.simple_public_object import SimplePublicObject

from hubspot_integration import hubspot_operations


@pytest.fixture(scope="function")
def do_search_mock_exist_provider() -> Generator[MagicMock, None, None]:
    with patch(
        "hubspot.crm.companies.SearchApi.do_search",
        return_value=CollectionResponseWithTotalSimplePublicObjectForwardPaging(
            paging=None,
            results=[
                SimplePublicObject(
                    archived=False,
                    archived_at=None,
                    created_at=datetime.datetime(
                        2021, 12, 27, 5, 59, 1, 263000, tzinfo=tzutc()
                    ),
                    id="755862794",
                    properties={
                        "address": "11 Generatorgatan",
                        "business_id": "2597465-3",
                        "city": "Arlandastad",
                        "country": "Sweden",
                        "createdate": "2021-12-27T05:59:01.263Z",
                        "description": "Aviator provides ground handling, "
                        "ramp, passenger, baggage "
                        "handling, load control, flight "
                        "operations and crew "
                        "administration services.",
                        "employee_count": "210",
                        "hs_lastmodifieddate": "2022-06-06T04:22:26.831Z",
                        "hs_object_id": "755862794",
                        "is_public": "false",
                        "name": "Aviator Airport Services Finland Oy",
                        "phone": "46 8 58 55 42 00",
                        "zip": "19560",
                    },
                    properties_with_history=None,
                    updated_at=datetime.datetime(
                        2022, 6, 6, 4, 22, 26, 831000, tzinfo=tzutc()
                    ),
                )
            ],
            total=1,
        ),
    ) as search:
        yield search


@pytest.fixture(scope="function")
def do_search_mock_empty() -> Generator[MagicMock, None, None]:
    with patch(
        "hubspot.crm.companies.SearchApi.do_search",
        return_value=CollectionResponseWithTotalSimplePublicObjectForwardPaging(
            paging=None, results=[], total=0
        ),
    ) as search:
        yield search


@pytest.fixture(scope="function")
def do_search_mock_exist_shop() -> Generator[MagicMock, None, None]:
    with patch(
        "hubspot.crm.companies.SearchApi.do_search",
        return_value=CollectionResponseWithTotalSimplePublicObjectForwardPaging(
            paging=None,
            results=[
                SimplePublicObject(
                    archived=False,
                    archived_at=None,
                    created_at=datetime.datetime(
                        2021, 4, 21, 11, 48, 8, 787000, tzinfo=tzutc()
                    ),
                    id="5907641870",
                    properties={
                        "address": "SÄHKÖTIE 5",
                        "business_id": "254128-9",
                        "city": "Vantaa",
                        "country": "Finland",
                        "createdate": "2021-04-21T11:48:08.787Z",
                        "description": "XXL Sport og Villmark er Nordens "
                        "største sportskjede. Vi tilbyr et "
                        "bredt sortiment av kjente "
                        "merkevarer på nett og i våre "
                        "mange varehus. Velkommen til en "
                        "hyggelig handel hos XXL!",
                        "employee_count": None,
                        "hs_lastmodifieddate": "2022-06-06T04:22:30.534Z",
                        "hs_object_id": "5907641870",
                        "name": "XXL",
                        "phone": "+358306075020",
                        "website": "xxl.fi",
                    },
                    properties_with_history=None,
                    updated_at=datetime.datetime(
                        2022, 6, 6, 4, 22, 30, 534000, tzinfo=tzutc()
                    ),
                )
            ],
            total=1,
        ),
    ) as search:
        yield search


def test_get_hubspot_company_info_case_exist_provider(
    do_search_mock_exist_provider: MagicMock,
) -> None:
    output = hubspot_operations.HubSpotProvider().get_hubspot_company_info(
        business_ids={"2597465-3"}
    )
    assert output == [
        {"2597465-3": {"hs_object_id": "755862794", "employee_count": "210"}}
    ]


def test_get_hubspot_company_info_case_empty_provider(
    do_search_mock_empty: MagicMock,
) -> None:
    output = hubspot_operations.HubSpotProvider().get_hubspot_company_info(
        business_ids={"2597465-3"}
    )
    assert output is None


def test_get_hubspot_company_info_case_exist_shop(
    do_search_mock_exist_shop: MagicMock,
) -> None:
    output = hubspot_operations.HubSpotProvider().get_hubspot_company_info(
        business_ids={"254128-9"}
    )
    assert output == [
        {"254128-9": {"hs_object_id": "5907641870", "employee_count": None}}
    ]


def test_get_hubspot_company_info_case_empty_shop(
    do_search_mock_empty: MagicMock,
) -> None:
    output = hubspot_operations.HubSpotShop().get_hubspot_company_info(
        business_ids={"254128-9"}
    )

    assert output is None


def test_get_objs_changed_last_minutes_case_exist_provider(
    do_search_mock_exist_provider: MagicMock,
) -> None:
    output = hubspot_operations.HubSpotProvider().get_objs_changed_last_minutes()
    assert output == [
        {
            "address": "11 Generatorgatan",
            "business_id": "2597465-3",
            "city": "Arlandastad",
            "country": "Sweden",
            "createdate": "2021-12-27T05:59:01.263Z",
            "description": "Aviator provides ground handling, "
            "ramp, passenger, baggage "
            "handling, load control, flight "
            "operations and crew "
            "administration services.",
            "employee_count": 210,
            "hs_lastmodifieddate": "2022-06-06T04:22:26.831Z",
            "hs_object_id": "755862794",
            "is_public": "false",
            "name": "Aviator Airport Services Finland Oy",
            "phone": "46 8 58 55 42 00",
            "zip": "19560",
        }
    ]


def test_get_objs_changed_last_minutes_case_empty_provider(
    do_search_mock_empty: MagicMock,
) -> None:
    output = hubspot_operations.HubSpotProvider().get_objs_changed_last_minutes()
    assert output is None


def test_get_objs_changed_last_minutes_case_exist_shop(
    do_search_mock_exist_shop: MagicMock,
) -> None:
    output = hubspot_operations.HubSpotShop().get_objs_changed_last_minutes()
    assert output == [
        {
            "address": "SÄHKÖTIE 5",
            "business_id": "254128-9",
            "city": "Vantaa",
            "country": "Finland",
            "createdate": "2021-04-21T11:48:08.787Z",
            "description": "XXL Sport og Villmark er Nordens "
            "største sportskjede. Vi tilbyr et "
            "bredt sortiment av kjente "
            "merkevarer på nett og i våre "
            "mange varehus. Velkommen til en "
            "hyggelig handel hos XXL!",
            "employee_count": None,
            "hs_lastmodifieddate": "2022-06-06T04:22:30.534Z",
            "hs_object_id": "5907641870",
            "name": "XXL",
            "phone": "+358306075020",
            "website": "xxl.fi",
        }
    ]


def test_get_objs_changed_last_minutes_case_empty_shop(
    do_search_mock_empty: MagicMock,
) -> None:
    output = hubspot_operations.HubSpotShop().get_objs_changed_last_minutes()
    assert output is None
