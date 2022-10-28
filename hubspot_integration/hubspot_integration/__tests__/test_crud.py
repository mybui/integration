import crud_base
import crud_provider
import crud_shop
import db
import hubspot_operations
import models

from . import test_data, test_hubspot

db.create_connection()


class TestCrud:
    @staticmethod
    def create_crud_objs():
        return crud_provider.CRUDProvider(
            models.Provider, table_name="providers"
        ), crud_shop.CRUDShop(models.Shop, table_name="shops")

    def set_up(self):
        db_batch = crud_base.start_batch()
        crud_provider_obj, crud_shop_obj = self.create_crud_objs()

        crud_provider_obj.create_for_hubspot_to_db_integration(
            db_batch=db_batch,
            hubspot_obj=test_data.provider_1,
            log_batch=None,
        )
        crud_shop_obj.create_for_hubspot_to_db_integration(
            db_batch=db_batch,
            hubspot_obj=test_data.shop_1,
            log_batch=None,
        )

        crud_base.end_batch(db_batch)

    def clean_up(self):
        crud_provider_obj, crud_shop_obj = self.create_crud_objs()

        provider_search_result = crud_provider_obj.get_many_by_business_id(
            business_id=test_data.provider_1["business_id"]
        )
        shop_search_result = crud_shop_obj.get_many_by_business_id(
            business_id=test_data.shop_1["business_id"]
        )
        provider_log_search_result = models.LogIntegration.objects(
            hubspotId=test_data.hubspot_test_provider_hs_object_id
        ).allow_filtering()
        shop_log_search_result = models.LogIntegration.objects(
            hubspotId=test_data.hubspot_test_shop_hs_object_id
        ).allow_filtering()

        if provider_search_result:
            for provider in provider_search_result:
                provider.objects(id=provider.id).delete()
        if shop_search_result:
            for shop in shop_search_result:
                shop.objects(id=shop.id).delete()
        if provider_log_search_result:
            for provider in provider_log_search_result:
                provider.objects(id=provider.id).delete()
        if shop_log_search_result:
            for shop in shop_log_search_result:
                shop.objects(id=shop.id).delete()

    def test_update_hubspot_company_info(self):
        self.clean_up()
        self.set_up()
        crud_provider_obj, crud_shop_obj = self.create_crud_objs()

        crud_provider_obj.update_hubspot_company_info(
            hubspot_company_info=test_data.provider_1_hubspot_company_info
        )
        crud_shop_obj.update_hubspot_company_info(
            hubspot_company_info=test_data.shop_1_hubspot_company_info
        )

        provider_search_result = crud_provider_obj.get_many_by_business_id(
            business_id=test_data.provider_1["business_id"]
        )
        shop_search_result = crud_shop_obj.get_many_by_business_id(
            business_id=test_data.shop_1["business_id"]
        )

        if len(provider_search_result) == 1:
            provider_output = (
                provider_search_result[0].hubspotId
                == test_data.provider_1_hubspot_company_info[0][
                    test_data.provider_1["business_id"]
                ]["hs_object_id"]
                and provider_search_result[0].employeeCount
                == test_data.provider_1_hubspot_company_info[0][
                    test_data.provider_1["business_id"]
                ]["employee_count"]
            )
        else:
            provider_output = None
        if len(shop_search_result) == 1:
            shop_output = (
                shop_search_result[0].hubspotId
                == test_data.shop_1_hubspot_company_info[0][
                    test_data.shop_1["business_id"]
                ]["hs_object_id"]
                and shop_search_result[0].employeeCount
                == test_data.shop_1_hubspot_company_info[0][
                    test_data.shop_1["business_id"]
                ]["employee_count"]
            )
        else:
            shop_output = None

        final_output = provider_output and shop_output
        self.clean_up()
        assert final_output == True

    def integrate_from_hubspot_to_db_set_up(self):
        crud_provider_obj, crud_shop_obj = self.create_crud_objs()

        crud_provider_obj.integrate_from_hubspot_to_db(
            objs_changed_last_15_minutes_in_hubspot=[
                obj
                for obj in hubspot_operations.HubSpotProvider().get_objs_changed_last_15_minutes(
                    skip_test_data=False
                )
                if obj["hs_object_id"] == test_data.hubspot_test_provider_hs_object_id
            ],
            duplicated_business_ids=crud_provider_obj.get_duplicated_business_ids(),
        )
        crud_shop_obj.integrate_from_hubspot_to_db(
            objs_changed_last_15_minutes_in_hubspot=[
                obj
                for obj in hubspot_operations.HubSpotShop().get_objs_changed_last_15_minutes(
                    skip_test_data=False
                )
                if obj["hs_object_id"] == test_data.hubspot_test_shop_hs_object_id
            ],
            duplicated_business_ids=crud_shop_obj.get_duplicated_business_ids(),
        )

        provider_search_result = crud_provider_obj.get_many_by_business_id(
            business_id=test_data.provider_1["business_id"]
        )
        shop_search_result = crud_shop_obj.get_many_by_business_id(
            business_id=test_data.shop_1["business_id"]
        )

        if len(provider_search_result) == 1:
            provider_output = (
                provider_search_result[0].employeeCount
                == test_data.hubspot_test_data["employee_count"]
            )
        else:
            provider_output = None
        if len(shop_search_result) == 1:
            shop_output = (
                shop_search_result[0].employeeCount
                == test_data.hubspot_test_data["employee_count"]
            )
        else:
            shop_output = None

        final_output = provider_output and shop_output
        return final_output

        # integration testing

    def test_integrate_from_hubspot_to_db_case_update(self):
        self.set_up()

        # call HubSpot module
        test_hubspot.TestHubSpot().set_up()

        # call CRUD module
        output = self.integrate_from_hubspot_to_db_set_up()
        self.clean_up()

        assert output == True

    def test_integrate_from_hubspot_to_db_case_create(self):
        test_hubspot.TestHubSpot().set_up()
        output = self.integrate_from_hubspot_to_db_set_up()
        self.clean_up()

        assert output == True
