# ruff: noqa: FBT002, PLR0913
import logging
from crm.serializers.company import CRMCompanySerializer
from crm.serializers.user import CRMUserSerializer
from crm.element_types import ElementTypes
from crm.vtiger import parsvt_crm
from utils.kafka import KafkaEventStore

logger = logging.getLogger(__name__)


class CompanyService:
    def __init__(self, event_store: KafkaEventStore):
        self.event_store = event_store

    @staticmethod
    def create_company(**kwargs):
        company_crm_data = parsvt_crm.serialize_and_create(
            element_type=ElementTypes.Company,
            crm_serializer_class=CRMCompanySerializer,
            **kwargs,
        )
        parsvt_crm.serialize_and_update(  # TODO make it a none-blocking task
            element_type=ElementTypes.User,
            crm_serializer_class=CRMUserSerializer,
            panel_id=kwargs["user"],
            account_id=company_crm_data["id"],
        )
        return company_crm_data

    @staticmethod
    def update_company(**kwargs):
        return parsvt_crm.serialize_and_update(
            element_type=ElementTypes.Company,
            panel_id=kwargs["id"],
            crm_serializer_class=CRMCompanySerializer,
            **kwargs,
        )

    @staticmethod
    def delete_company(**kwargs):
        panel_id = kwargs["id"]
        company_crm_data = parsvt_crm.retrieve_by_panel_id(
            element_type=ElementTypes.Company, panel_id=panel_id
        )
        crm_id = company_crm_data["id"]
        assert crm_id, "crm_id is required for delete!"
        return parsvt_crm.delete(crm_id=crm_id)
