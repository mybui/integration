from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

import core.models as models
from webflow_integration import webflow_models, webflow_operations


@pytest.fixture(scope="function")
def item_partner_mock() -> Generator[MagicMock, None, None]:
    with patch(
        "webflowpy.Webflow.Webflow.items",
        return_value={
            "items": [
                {
                    "website": "https://sevenbikes.fi/",
                    "_archived": False,
                    "_draft": False,
                    "name": "Seven Bikes",
                    "slug": "seven-bikes",
                    "location-s-2": ["619d0ff1988395c88831f5fe"],
                    "updated-on": "2022-05-30T13:40:35.739Z",
                    "updated-by": "Person_60914bca1e84500a32ef0218",
                    "created-on": "2022-02-14T10:56:16.641Z",
                    "created-by": "Person_60914bca1e84500a32ef0218",
                    "published-on": "2022-05-30T14:54:36.040Z",
                    "published-by": "Person_60914bca1e84500a32ef0218",
                    "locations": "Tampere",
                    "business-id": "3215327-1",
                    "_cid": "619d0ff1988395dd1b31f4ab",
                    "_id": "620a3550460a0877e660247d",
                }
            ],
            "count": 1,
            "limit": 100,
            "offset": 0,
            "total": 1,
        },
    ) as items:
        yield items


@pytest.fixture(scope="function")
def item_partner_city_mock() -> Generator[MagicMock, None, None]:
    with patch(
        "webflowpy.Webflow.Webflow.items",
        return_value={
            "items": [
                {
                    "_archived": False,
                    "_draft": False,
                    "name": "Stockholm",
                    "slug": "stockholm",
                    "updated-on": "2022-06-01T06:55:53.969Z",
                    "updated-by": "Person_60914bca1e84500a32ef0218",
                    "created-on": "2022-06-01T06:55:53.969Z",
                    "created-by": "Person_60914bca1e84500a32ef0218",
                    "published-on": "2022-06-01T06:55:53.969Z",
                    "published-by": "Person_60914bca1e84500a32ef0218",
                    "_cid": "619d0ff19883953bf531f4b2",
                    "_id": "62970d79a86935182000dcdc",
                }
            ],
            "count": 1,
            "limit": 100,
            "offset": 0,
            "total": 1,
        },
    ) as items:
        yield items


@pytest.fixture(scope="function")
def item_mock_empty() -> Generator[MagicMock, None, None]:
    with patch(
        "webflowpy.Webflow.Webflow.items",
        return_value={"items": [], "count": 0, "limit": 100, "offset": 0, "total": 0},
    ) as items:
        yield items


@pytest.fixture(scope="function")
def create_partner_mock_okay() -> Generator[MagicMock, None, None]:
    with patch(
        "webflowpy.Webflow.Webflow.createItem",
        return_value={
            "_archived": False,
            "_draft": False,
            "name": "Test partner 1",
            "business-id": "business-id-test-1",
            "locations": "Imatra",
            "slug": "test-partner-1",
            "location-s-2": ["619d0ff19883951f7f31f5e9"],
            "updated-on": "2022-06-08T08:06:33.412Z",
            "updated-by": "Person_60914bca1e84500a32ef0218",
            "created-on": "2022-06-08T08:06:33.412Z",
            "created-by": "Person_60914bca1e84500a32ef0218",
            "published-on": "2022-06-08T08:06:33.412Z",
            "published-by": "Person_60914bca1e84500a32ef0218",
            "_cid": "619d0ff1988395dd1b31f4ab",
            "_id": "62a05fe5a4ad8c3b4c21bc08",
        },
    ) as items:
        yield items


@pytest.fixture(scope="function")
def create_partner_mock_error() -> Generator[MagicMock, None, None]:
    with patch(
        "webflowpy.Webflow.Webflow.createItem",
        return_value={
            "msg": "'fields.slug' invalid input",
            "code": 400,
            "name": "ValidationError",
            "path": "/collections/619d0ff1988395dd1b31f4ab/items",
            "err": "ValidationError: 'fields.slug' invalid input",
        },
    ) as items:
        yield items


@pytest.fixture(scope="function")
def create_partner_city_mock_okay() -> Generator[MagicMock, None, None]:
    with patch(
        "webflowpy.Webflow.Webflow.createItem",
        return_value={
            "_archived": False,
            "_draft": False,
            "name": "Hanko",
            "slug": "hanko",
            "updated-on": "2022-06-08T07:17:12.358Z",
            "updated-by": "Person_60914bca1e84500a32ef0218",
            "created-on": "2022-06-08T07:17:12.358Z",
            "created-by": "Person_60914bca1e84500a32ef0218",
            "published-on": "2022-06-08T07:17:12.358Z",
            "published-by": "Person_60914bca1e84500a32ef0218",
            "_cid": "619d0ff19883953bf531f4b2",
            "_id": "62a04cf883df8847df6a8159",
        },
    ) as items:
        yield items


@pytest.fixture(scope="function")
def create_partner_city_mock_error() -> Generator[MagicMock, None, None]:
    with patch(
        "webflowpy.Webflow.Webflow.createItem",
        return_value={
            "msg": "Validation Failure",
            "code": 400,
            "name": "ValidationError",
            "path": "/collections/619d0ff19883953bf531f4b2/items",
            "err": "ValidationError: Validation Failure",
            "problems": [
                "Field 'slug': Unique value is already in database: 'test-partner-city-1'"
            ],
            "problem_data": [
                {
                    "slug": "slug",
                    "msg": "Unique value is already in database",
                    "value": "'test-partner-city-1'",
                }
            ],
            "extensions": {
                "input": {
                    "collection_id": {
                        "_bsontype": "ObjectID",
                        "id": {
                            "0": 97,
                            "1": 157,
                            "2": 15,
                            "3": 241,
                            "4": 152,
                            "5": 131,
                            "6": 149,
                            "7": 59,
                            "8": 245,
                            "9": 49,
                            "10": 244,
                            "11": 178,
                        },
                    },
                    "item_id": None,
                    "target": "live",
                    "mode": "live",
                    "need_staging": True,
                    "need_live": True,
                    "need_collections": False,
                    "need_staging_draft": False,
                    "isPatchMode": False,
                    "isSilentMode": False,
                    "skipInvalidFiles": False,
                },
                "meta": {
                    "authType": "oauth_user",
                    "userId": {
                        "_bsontype": "ObjectID",
                        "id": {
                            "0": 96,
                            "1": 145,
                            "2": 75,
                            "3": 202,
                            "4": 30,
                            "5": 132,
                            "6": 80,
                            "7": 10,
                            "8": 50,
                            "9": 239,
                            "10": 2,
                            "11": 24,
                        },
                    },
                },
            },
        },
    ) as items:
        yield items


@pytest.fixture(scope="function")
def update_partner_mock_okay() -> Generator[MagicMock, None, None]:
    with patch(
        "webflowpy.Webflow.Webflow.patchItem",
        return_value={
            "_archived": False,
            "_draft": False,
            "name": "Test partner 2",
            "business-id": "business-id-test-1",
            "locations": "Stockholm",
            "slug": "test-partner-2",
            "location-s-2": ["62970d79a86935182000dcdc"],
            "updated-on": "2022-06-08T08:40:15.880Z",
            "updated-by": "Person_60914bca1e84500a32ef0218",
            "created-on": "2022-06-08T08:37:57.706Z",
            "created-by": "Person_60914bca1e84500a32ef0218",
            "published-on": "2022-06-08T08:40:15.880Z",
            "published-by": "Person_60914bca1e84500a32ef0218",
            "_cid": "619d0ff1988395dd1b31f4ab",
            "_id": "62a05fe5a4ad8c3b4c21bc08",
        },
    ) as items:
        yield items


@pytest.fixture(scope="function")
def update_partner_mock_error() -> Generator[MagicMock, None, None]:
    with patch(
        "webflowpy.Webflow.Webflow.patchItem",
        return_value={
            "msg": "'fields.slug' invalid input",
            "code": 400,
            "name": "ValidationError",
            "path": "/collections/619d0ff1988395dd1b31f4ab/items",
            "err": "ValidationError: 'fields.slug' invalid input",
        },
    ) as items:
        yield items


# tests
def test_get_all_partners_case_exist(item_partner_mock: MagicMock) -> None:
    output = webflow_operations.WebflowCollectionBase().get_all_partners()
    assert output == [
        {
            "website": "https://sevenbikes.fi/",
            "_archived": False,
            "_draft": False,
            "name": "Seven Bikes",
            "slug": "seven-bikes",
            "location-s-2": ["619d0ff1988395c88831f5fe"],
            "updated-on": "2022-05-30T13:40:35.739Z",
            "updated-by": "Person_60914bca1e84500a32ef0218",
            "created-on": "2022-02-14T10:56:16.641Z",
            "created-by": "Person_60914bca1e84500a32ef0218",
            "published-on": "2022-05-30T14:54:36.040Z",
            "published-by": "Person_60914bca1e84500a32ef0218",
            "locations": "Tampere",
            "business-id": "3215327-1",
            "_cid": "619d0ff1988395dd1b31f4ab",
            "_id": "620a3550460a0877e660247d",
        }
    ]


def test_get_all_partners_case_empty(item_mock_empty: MagicMock) -> None:
    output = webflow_operations.WebflowCollectionBase().get_all_partners()
    assert output is None


def test_get_all_partner_cities_case_exist(item_partner_city_mock: MagicMock) -> None:
    output = webflow_operations.WebflowCollectionBase().get_all_partner_cities()
    assert output == [
        {
            "_archived": False,
            "_draft": False,
            "name": "Stockholm",
            "slug": "stockholm",
            "updated-on": "2022-06-01T06:55:53.969Z",
            "updated-by": "Person_60914bca1e84500a32ef0218",
            "created-on": "2022-06-01T06:55:53.969Z",
            "created-by": "Person_60914bca1e84500a32ef0218",
            "published-on": "2022-06-01T06:55:53.969Z",
            "published-by": "Person_60914bca1e84500a32ef0218",
            "_cid": "619d0ff19883953bf531f4b2",
            "_id": "62970d79a86935182000dcdc",
        }
    ]


def test_get_all_partner_cities_case_empty(item_mock_empty: MagicMock) -> None:
    output = webflow_operations.WebflowCollectionBase().get_all_partner_cities()
    assert output is None


def test_get_a_partner_case_exist(item_partner_mock: MagicMock) -> None:
    output = webflow_operations.WebflowCollectionBase().get_a_partner(
        item_id="620a3550460a0877e660247d"
    )
    assert output == {
        "website": "https://sevenbikes.fi/",
        "_archived": False,
        "_draft": False,
        "name": "Seven Bikes",
        "slug": "seven-bikes",
        "location-s-2": ["619d0ff1988395c88831f5fe"],
        "updated-on": "2022-05-30T13:40:35.739Z",
        "updated-by": "Person_60914bca1e84500a32ef0218",
        "created-on": "2022-02-14T10:56:16.641Z",
        "created-by": "Person_60914bca1e84500a32ef0218",
        "published-on": "2022-05-30T14:54:36.040Z",
        "published-by": "Person_60914bca1e84500a32ef0218",
        "locations": "Tampere",
        "business-id": "3215327-1",
        "_cid": "619d0ff1988395dd1b31f4ab",
        "_id": "620a3550460a0877e660247d",
    }


def test_get_a_partner_case_empty(item_mock_empty: MagicMock) -> None:
    output = webflow_operations.WebflowCollectionBase().get_a_partner(
        item_id="620a3550460a0877e660247ddd"
    )
    assert output is None


def test_create_a_partner_city_case_okay(
    create_partner_city_mock_okay: MagicMock,
) -> None:
    output = webflow_operations.WebflowCollectionBase().create_a_partner_city(
        item_data=webflow_models.WebflowPartnerCityCreate(
            **{"name": "Hanko", "slug": "hanko"}
        ).dict(by_alias=True)
    )
    assert output == {
        "_archived": False,
        "_draft": False,
        "name": "Hanko",
        "slug": "hanko",
        "updated-on": "2022-06-08T07:17:12.358Z",
        "updated-by": "Person_60914bca1e84500a32ef0218",
        "created-on": "2022-06-08T07:17:12.358Z",
        "created-by": "Person_60914bca1e84500a32ef0218",
        "published-on": "2022-06-08T07:17:12.358Z",
        "published-by": "Person_60914bca1e84500a32ef0218",
        "_cid": "619d0ff19883953bf531f4b2",
        "_id": "62a04cf883df8847df6a8159",
    }


def test_create_a_partner_city_case_error(
    create_partner_city_mock_error: MagicMock,
) -> None:
    output = webflow_operations.WebflowCollectionBase().create_a_partner_city(
        item_data=webflow_models.WebflowPartnerCityCreate(
            **{"name": "Test partner city 1", "slug": "test-partner-city-1"}
        ).dict(by_alias=True)
    )
    assert output is None


def test_get_a_partner_city_id_case_exist_and_okay(
    item_partner_city_mock: MagicMock, create_partner_city_mock_okay: MagicMock
) -> None:
    output = webflow_operations.WebflowCollectionBase().get_partner_city_id(
        locations=["Hanko"]
    )
    assert output == ["62a04cf883df8847df6a8159"]


def test_get_a_partner_city_id_case_exist_and_error(
    item_partner_city_mock: MagicMock, create_partner_city_mock_error: MagicMock
) -> None:
    output = webflow_operations.WebflowCollectionBase().get_partner_city_id(
        locations=["Hanko"]
    )
    assert output == []


def test_get_a_partner_city_id_case_empty_and_okay(
    item_mock_empty: MagicMock, create_partner_city_mock_okay: MagicMock
) -> None:
    output = webflow_operations.WebflowCollectionBase().get_partner_city_id(
        locations=["Hanko"]
    )
    assert output == ["62a04cf883df8847df6a8159"]


def test_get_a_partner_city_id_case_empty_and_error(
    item_mock_empty: MagicMock, create_partner_city_mock_error: MagicMock
) -> None:
    output = webflow_operations.WebflowCollectionBase().get_partner_city_id(
        locations=["Hanko"]
    )
    assert output == []


def test_create_a_partner_case_okay(create_partner_mock_okay: MagicMock) -> None:
    output = webflow_operations.WebflowCollectionBase().create_a_partner(
        item_data=(
            webflow_models.WebflowPartnerCreate(
                **{
                    "name": "Test partner 1",
                    "business-id": "business-id-test-1",
                    "locations": "Imatra",
                    "slug": "test-partner-1",
                    "location-s-2": ["619d0ff19883951f7f31f5e9"],
                }
            ).dict(by_alias=True)
        )
    )
    assert output == {
        "_archived": False,
        "_draft": False,
        "name": "Test partner 1",
        "business-id": "business-id-test-1",
        "locations": "Imatra",
        "slug": "test-partner-1",
        "location-s-2": ["619d0ff19883951f7f31f5e9"],
        "updated-on": "2022-06-08T08:06:33.412Z",
        "updated-by": "Person_60914bca1e84500a32ef0218",
        "created-on": "2022-06-08T08:06:33.412Z",
        "created-by": "Person_60914bca1e84500a32ef0218",
        "published-on": "2022-06-08T08:06:33.412Z",
        "published-by": "Person_60914bca1e84500a32ef0218",
        "_cid": "619d0ff1988395dd1b31f4ab",
        "_id": "62a05fe5a4ad8c3b4c21bc08",
    }


def test_create_a_partner_case_error(create_partner_mock_error: MagicMock) -> None:
    output = webflow_operations.WebflowCollectionBase().create_a_partner(
        item_data=(
            webflow_models.WebflowPartnerCreate(
                **{
                    "name": "Test partner 1",
                    "business-id": "business-id-test-1",
                    "locations": "Imatra",
                    "slug": "test-pärtner-1",
                    "location-s-2": ["619d0ff19883951f7f31f5e9"],
                }
            ).dict(by_alias=True)
        )
    )
    assert output is None


def test_update_a_partner_case_okay(update_partner_mock_okay: MagicMock) -> None:
    output = webflow_operations.WebflowCollectionBase().update_a_partner(
        item_id="62a05889c3ef87b9d2433e26",
        item_data=(
            webflow_models.WebflowPartnerUpdate(
                **{
                    "business-id": "business-id-test-1",
                    "name": "Test partner 2",
                    "locations": "Stockholm",
                    "slug": "test-partner-2",
                    "location-s-2": ["62970d79a86935182000dcdc"],
                }
            ).dict(by_alias=True)
        ),
    )
    assert output == {
        "_archived": False,
        "_draft": False,
        "name": "Test partner 2",
        "business-id": "business-id-test-1",
        "locations": "Stockholm",
        "slug": "test-partner-2",
        "location-s-2": ["62970d79a86935182000dcdc"],
        "updated-on": "2022-06-08T08:40:15.880Z",
        "updated-by": "Person_60914bca1e84500a32ef0218",
        "created-on": "2022-06-08T08:37:57.706Z",
        "created-by": "Person_60914bca1e84500a32ef0218",
        "published-on": "2022-06-08T08:40:15.880Z",
        "published-by": "Person_60914bca1e84500a32ef0218",
        "_cid": "619d0ff1988395dd1b31f4ab",
        "_id": "62a05fe5a4ad8c3b4c21bc08",
    }


def test_update_a_partner_case_error(update_partner_mock_error: MagicMock) -> None:
    output = webflow_operations.WebflowCollectionBase().update_a_partner(
        item_id="62a05889c3ef87b9d2433e26",
        item_data=(
            webflow_models.WebflowPartnerUpdate(
                **{
                    "business-id": "business-id-test-1",
                    "name": "Test partner 2",
                    "locations": "Stockholm",
                    "slug": "test-pärtner-2",
                    "location-s-2": ["62970d79a86935182000dcdc"],
                }
            ).dict(by_alias=True)
        ),
    )
    assert output is None


def test_update_for_webflow_to_db_integration_case_okay(
    update_partner_mock_okay: MagicMock,
) -> None:
    output = (
        webflow_operations.WebflowCollectionBase().update_for_webflow_to_db_integration(
            db_obj_info=(
                "a121a180-bcce-4d62-8939-7aed4457391f",
                "business-id-test-1",
                "62a05fe5a4ad8c3b4c21bc08",
            ),
            different_values={
                "name": "Test partner 2",
                "locations": "Stockholm",
                "slug": "test-partner-2",
                "location-s-2": ["62970d79a86935182000dcdc"],
            },
        )
    )
    assert output is True


def test_update_for_webflow_to_db_integration_case_error(
    update_partner_mock_error: MagicMock,
) -> None:
    output = (
        webflow_operations.WebflowCollectionBase().update_for_webflow_to_db_integration(
            db_obj_info=(
                "a121a180-bcce-4d62-8939-7aed4457391f",
                "business-id-test-1",
                "62a05fe5a4ad8c3b4c21bc08",
            ),
            different_values={
                "name": "Test partner 2",
                "locations": "Stockholm",
                "slug": "test-pärtner-2",
                "location-s-2": ["62970d79a86935182000dcdc"],
            },
        )
    )
    assert output is False


def test_create_for_webflow_to_db_integration_case_okay(
    item_partner_city_mock: MagicMock,
    create_partner_city_mock_okay: MagicMock,
    create_partner_mock_okay: MagicMock,
) -> None:
    output = (
        webflow_operations.WebflowCollectionBase().create_for_webflow_to_db_integration(
            db_obj=models.Shop(
                id="a121a180-bcce-4d62-8939-7aed4457391f",
                name="Test partner 1",
                businessId="business-id-test-1",
                city="Imatra",
            ),
            db_batch=None,
            log_batch=None,
        )
    )
    assert output is True


def test_create_for_webflow_to_db_integration_case_empty_1(
    item_mock_empty: MagicMock,
    create_partner_city_mock_okay: MagicMock,
    create_partner_mock_okay: MagicMock,
) -> None:
    output = (
        webflow_operations.WebflowCollectionBase().create_for_webflow_to_db_integration(
            db_obj=models.Shop(
                id="a121a180-bcce-4d62-8939-7aed4457391f",
                name="Test partner 1",
                businessId="business-id-test-1",
                city="Imatra",
            ),
            db_batch=None,
            log_batch=None,
        )
    )
    assert output is True


def test_create_for_webflow_to_db_integration_case_empty_2(
    item_mock_empty: MagicMock,
    create_partner_city_mock_error: MagicMock,
    create_partner_mock_okay: MagicMock,
) -> None:
    output = (
        webflow_operations.WebflowCollectionBase().create_for_webflow_to_db_integration(
            db_obj=models.Shop(
                id="a121a180-bcce-4d62-8939-7aed4457391f",
                name="Test partner 1",
                businessId="business-id-test-1",
                city="Test Partner City 1",
            ),
            db_batch=None,
            log_batch=None,
        )
    )
    assert output is True


def test_create_for_webflow_to_db_integration_case_error(
    item_partner_city_mock: MagicMock,
    create_partner_city_mock_okay: MagicMock,
    create_partner_mock_error: MagicMock,
) -> None:
    output = (
        webflow_operations.WebflowCollectionBase().create_for_webflow_to_db_integration(
            db_obj=models.Shop(
                id="a121a180-bcce-4d62-8939-7aed4457391f",
                name="Test partner 1",
                businessId="business-id-test-1",
                city="Imatra",
            ),
            db_batch=None,
            log_batch=None,
        )
    )
    assert output is False
