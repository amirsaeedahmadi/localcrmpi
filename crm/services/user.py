# ruff: noqa: FBT002, PLR0913
import logging
from crm.serializers.user import CRMUserSerializer
from crm.element_types import ElementTypes
from crm.vtiger import parsvt_crm

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def create_user(**user_data):
        if crm_id := user_data.get("crm_id"):
            panel_id = user_data["id"]
            user_element_type = (
                ElementTypes.Personnel
                if user_data.get("is_crm_personnel")
                else ElementTypes.User
            )
            update_panel_id_result = parsvt_crm.update(
                element_type=user_element_type,
                element_crm_data={"id": crm_id},  # personnel_crm_data,
                **{user_element_type.panel_id_field: panel_id},
            )
            return update_panel_id_result
        user_crm_data = parsvt_crm.serialize_and_create(
            element_type=ElementTypes.User,
            crm_serializer_class=CRMUserSerializer,
            **user_data,
        )
        return user_crm_data

    @staticmethod
    def update_user(**user_data):
        return parsvt_crm.serialize_and_update(
            element_type=ElementTypes.User,
            crm_serializer_class=CRMUserSerializer,
            panel_id=user_data["id"],
            **user_data,
        )

    @staticmethod
    def delete_user(**kwargs):
        panel_id = kwargs["id"]
        crm_user_data = parsvt_crm.retrieve_by_panel_id(
            element_type=ElementTypes.User, panel_id=panel_id
        )
        crm_id = crm_user_data["id"]
        assert crm_id, "crm_id is required for delete!"
        return parsvt_crm.delete(crm_id=crm_id)
