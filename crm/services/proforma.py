# ruff: noqa: FBT002, PLR0913
import logging
from crm.serializers.proforma import CRMProformaSerializer, ImportCRMProformaSerializer
from crm.serializers.line_item import LineItemSerializer
from crm.element_types import ElementTypes
from crm.vtiger import parsvt_crm
from crm.events import ProformaUpdated, ProformaDeleted, CRMProformaCreated

logger = logging.getLogger(__name__)


class ProformaService:
    def __init__(self, evert_store):
        self.event_store = evert_store

    @staticmethod
    def create_proforma(**kwargs):
        proforma_crm_data = parsvt_crm.serialize_and_create(
            element_type=ElementTypes.Proforma,
            crm_serializer_class=CRMProformaSerializer,
            **kwargs,
        )
        return proforma_crm_data

    @staticmethod
    def update_proforma(**kwargs):
        return parsvt_crm.serialize_and_update(
            element_type=ElementTypes.Proforma,
            panel_id=kwargs["id"],
            crm_serializer_class=CRMProformaSerializer,
            **kwargs,
        )

    @staticmethod
    def delete_proforma(**kwargs):
        panel_id = kwargs["id"]
        proforma_crm_data = parsvt_crm.retrieve_by_panel_id(
            element_type=ElementTypes.Proforma, panel_id=panel_id
        )
        crm_id = proforma_crm_data["id"]
        assert crm_id, "crm_id is required for delete!"
        return parsvt_crm.delete(crm_id=crm_id)

    def on_proforma_created(self, **proforma_data):
        proforma_serializer = ImportCRMProformaSerializer(data=proforma_data)
        proforma_serializer.is_valid(raise_exception=True)
        event = CRMProformaCreated(proforma_serializer.validated_data)
        self.event_store.add_event(event)
        return proforma_serializer.validated_data

    def on_proforma_updated(self, **proforma_data):
        proforma_serializer = ImportCRMProformaSerializer(data=proforma_data)
        proforma_serializer.is_valid(raise_exception=True)
        event = ProformaUpdated(proforma_serializer.validated_data)
        self.event_store.add_event(event)
        return proforma_serializer.validated_data

    def publish_deleted(self, **proforma_data):
        proforma_serializer = ImportCRMProformaSerializer(data=proforma_data)
        proforma_serializer.is_valid(raise_exception=True)
        event = ProformaDeleted(proforma_serializer.validated_data)
        self.event_store.add_event(event)
        return proforma_serializer.validated_data

    def on_crm_proforma_created(self, **body):
        crm_id = body["crm_id"]
        panel_id = body["id"]
        proforma_crm_data = parsvt_crm.retrieve(ElementTypes.Proforma, crm_id=crm_id)[0]
        find_items_where_clause = f"WHERE parent_id = {proforma_crm_data['id']}"
        proforma_line_items_crm_data = parsvt_crm.retrieve(
            ElementTypes.LineItem, where_clause=find_items_where_clause
        )
        line_item_serializer = LineItemSerializer(
            data=proforma_line_items_crm_data, many=True
        )
        line_item_serializer.is_valid(raise_exception=True)
        proforma_crm_data["items"] = line_item_serializer.validated_data
        proforma_crm_data[ElementTypes.Proforma.panel_id_field] = panel_id
        return parsvt_crm.update(
            element_type=ElementTypes.Proforma,
            element_crm_data=proforma_crm_data,
            **{ElementTypes.Proforma.panel_id_field: panel_id},
        )
