# ruff: noqa: FBT002, PLR0913
import logging
from crm.serializers.service_request import (
    CRMServiceRequestSerializer,
    ImportCRMServiceRequestSerializer,
)
from crm.serializers.enum import PanelServiceRequestStatusChoices
from crm.element_types import ElementTypes
from crm.vtiger import parsvt_crm
from crm.events import ServiceRequestInspected
from utils.kafka import KafkaEventStore

logger = logging.getLogger(__name__)


class ServiceRequestService:
    def __init__(self, event_store: KafkaEventStore):
        self.event_store = event_store

    @staticmethod
    def create_service_request(**kwargs):
        service_request_crm_data = parsvt_crm.serialize_and_create(
            element_type=ElementTypes.ServiceRequest,
            crm_serializer_class=CRMServiceRequestSerializer,
            **kwargs,
        )
        return service_request_crm_data

    @staticmethod
    def update_service_request(**kwargs):
        return parsvt_crm.serialize_and_update(
            element_type=ElementTypes.ServiceRequest,
            panel_id=kwargs["id"],
            crm_serializer_class=CRMServiceRequestSerializer,
            **kwargs,
        )

    @staticmethod
    def delete_service_request(**kwargs):
        panel_id = kwargs["id"]
        service_request_crm_data = parsvt_crm.retrieve_by_panel_id(
            element_type=ElementTypes.ServiceRequest, panel_id=panel_id
        )
        crm_id = service_request_crm_data["id"]
        assert crm_id, "crm_id is required for delete!"
        return parsvt_crm.delete(crm_id=crm_id)

    def on_inspected(self, **service_request_data):
        service_request_data["status"] = PanelServiceRequestStatusChoices.INSPECTING
        service_request_serializer = ImportCRMServiceRequestSerializer(
            data=service_request_data
        )
        service_request_serializer.is_valid(raise_exception=True)
        event = ServiceRequestInspected(
            service_request_serializer.validated_data
        )  # todo maybe better to use Updated event
        self.event_store.add_event(event)
        return service_request_serializer.validated_data
