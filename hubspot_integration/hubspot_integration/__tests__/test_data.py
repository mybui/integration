import random

provider_1 = {
    "address": "1730 South U.S Highway 31",
    "business_id": "businessId1",
    "city": "Greenwood",
    "country": "United States",
    "name": "Test Test Company",
    "is_public": False,
}

shop_1 = {
    "address": "1729 South U.S Highway 31",
    "business_id": "businessId2",
    "city": "Greenwood",
    "country": "United States",
    "name": "Test Test Shop",
}

provider_1_hubspot_company_info = [
    {
        provider_1["business_id"]: {
            "hs_object_id": "8834903438",
            "employee_count": 200,
        }
    },
]

shop_1_hubspot_company_info = [
    {
        shop_1["business_id"]: {
            "hs_object_id": "8843173453",
            "employee_count": 100,
        }
    },
]

hubspot_test_provider_hs_object_id = provider_1_hubspot_company_info[0][
    provider_1["business_id"]
]["hs_object_id"]

hubspot_test_shop_hs_object_id = shop_1_hubspot_company_info[0][shop_1["business_id"]][
    "hs_object_id"
]

hubspot_test_provider_business_id = provider_1["business_id"]

hubspot_test_shop_business_id = shop_1["business_id"]

hubspot_test_data = {"employee_count": random.randint(10, 1000)}
