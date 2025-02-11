# ruff: noqa: FBT002, PLR0913
import logging
from crm.serializers.personnel import (
    ImportCRMPersonnelSerializer,
    CRMPersonnelSerializer,
)
from crm.element_types import ElementTypes
from crm.vtiger import parsvt_crm
from utils.kafka import KafkaEventStore
from crm.events import UserCreated, UserUpdated, UserDeleted

logger = logging.getLogger(__name__)


class PersonnelService:
    def __init__(self, event_store: KafkaEventStore):
        self.event_store = event_store

    def on_personnel_created(self, **personnel_data):
        personnel_serializer = ImportCRMPersonnelSerializer(data=personnel_data)
        personnel_serializer.is_valid(raise_exception=True)
        event = UserCreated(personnel_serializer.validated_data)
        self.event_store.add_event(event)
        return personnel_serializer.validated_data

    def on_personnel_updated(self, **personnel_data):
        personnel_serializer = ImportCRMPersonnelSerializer(data=personnel_data)
        personnel_serializer.is_valid(raise_exception=True)
        event = UserUpdated(personnel_serializer.validated_data)
        self.event_store.add_event(event)
        return personnel_serializer.validated_data

    def publish_deleted(self, **personnel_data):
        personnel_serializer = ImportCRMPersonnelSerializer(data=personnel_data)
        personnel_serializer.is_valid(raise_exception=True)
        event = UserDeleted(personnel_serializer.validated_data)
        self.event_store.add_event(event)
        return personnel_serializer.validated_data

    @staticmethod
    def create_personnel(**personnel_data):
        personnel_crm_data = parsvt_crm.serialize_and_create(
            element_type=ElementTypes.Personnel,
            crm_serializer_class=CRMPersonnelSerializer,
            **personnel_data,
        )
        return personnel_crm_data

    @staticmethod
    def update_personnel(**personnel_data):
        return parsvt_crm.serialize_and_update(
            element_type=ElementTypes.Personnel,
            crm_serializer_class=CRMPersonnelSerializer,
            panel_id=personnel_data["id"],
            **personnel_data,
        )

    @staticmethod
    def delete_personnel(**kwargs):
        panel_id = kwargs["id"]
        crm_personnel_data = parsvt_crm.retrieve_by_panel_id(
            element_type=ElementTypes.Personnel, panel_id=panel_id
        )
        crm_id = crm_personnel_data["id"]
        assert crm_id, "crm_id is required for delete!"
        return parsvt_crm.delete(crm_id=crm_id)
