import json
import logging
import requests
import base64
from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth
from crm.element_types import ElementTypes, ElementType

from django.conf import settings

logger = logging.getLogger(__name__)
SUCCESS_CODE = 200


class ParsVTCRM:
    base_url = settings.CRM_SETTINGS.get("CRM_BASE_API_URL")
    username = settings.CRM_SETTINGS.get("CRM_ADMIN_USERNAME")
    password = settings.CRM_SETTINGS.get("CRM_ADMIN_PASSWORD")

    def __init__(self, base_url=None, username=None, password=None):
        self.base_url = base_url or self.base_url
        self.username = username or self.username
        self.password = password or self.password
        assert self.base_url, "crm base_url is required!"
        assert self.username, "crm username is required!"
        assert self.password, "crm password is required!"

    @property
    def authorization_code(self):
        return HTTPBasicAuth(username=self.username, password=self.password)

    def retrieve(self, element_type: ElementType, crm_id=None, where_clause=""):
        where_clause = f"WHERE id = '{crm_id}'" if crm_id else where_clause
        query = f"SELECT * from {element_type.name} {where_clause};"  # noqa: S608
        data = {"query": query}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.get(
            url=f"{self.base_url}/extended/query",
            data=urlencode(data),
            headers=headers,
            auth=self.authorization_code,
            timeout=5,
        )
        response.raise_for_status()
        return response.json()["result"]

    def create(self, element_type: ElementType, element_data: dict):
        data = {"elementType": element_type.name, "element": json.dumps(element_data)}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            url=f"{self.base_url}/extended/parsvt_create",
            data=urlencode(data),
            headers=headers,
            auth=self.authorization_code,
            timeout=5,
        )
        response.raise_for_status()
        return response.json()["result"]

    def update(
        self, element_type: ElementType, crm_id=None, element_crm_data=None, **new_data
    ):
        assert (
            element_crm_data or crm_id
        ), "element_crm_data or crm_id is required for update"
        element_crm_data = (
            element_crm_data
            or self.retrieve(element_type=element_type, crm_id=crm_id)[0]
        )
        assert (
            element_crm_data
        ), f"Element of {element_type.name} with id: {crm_id} doesn't exists in crm!"
        updated_element_crm_data = element_crm_data.copy()
        updated_element_crm_data.update(new_data)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "element": json.dumps(updated_element_crm_data),
            "elementType": element_type.name,
        }
        url = f"{self.base_url}/extended/"
        url += "updateInventory" if element_type.is_inventory_model else "revise"
        response = requests.post(
            url=url,
            data=urlencode(data),
            headers=headers,
            auth=self.authorization_code,
            timeout=5,
        )
        response.raise_for_status()
        return response.json()["result"]

    def delete(self, crm_id):
        data = {"id": crm_id}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            url=f"{self.base_url}/extended/delete",
            data=urlencode(data),
            headers=headers,
            auth=self.authorization_code,
            timeout=5,
        )
        response.raise_for_status()
        return response.json()

    def retrieve_contact_by_email(self, email):
        where_clause = f"WHERE email = '{email}'"
        user = self.retrieve(ElementTypes.User, where_clause=where_clause)
        return user[0] if user else None

    def retrieve_by_panel_id(self, element_type, panel_id):
        where_clause = "WHERE {element_type_panel_id_field} = '{panel_id}'"
        where_clause = where_clause.format(
            element_type_panel_id_field=element_type.panel_id_field, panel_id=panel_id
        )
        crm_entity = self.retrieve(element_type=element_type, where_clause=where_clause)
        return crm_entity[0] if crm_entity else None

    def update_by_panel_id(self, element_type, panel_id, **new_data):
        element_crm_data = self.retrieve_by_panel_id(
            element_type=element_type, panel_id=panel_id
        )
        return self.update(
            element_type=element_type, element_crm_data=element_crm_data, **new_data
        )

    def create_contact(self, contact_data: dict):
        return self.create(ElementTypes.User, contact_data)

    def serialize_and_update(
        self,
        element_type: ElementType,
        crm_serializer_class,
        crm_id=None,
        panel_id=None,
        **new_data,
    ):
        assert crm_id or panel_id, "crm_id or panel_id is required!"
        element_crm_data = (
            None
            if crm_id
            else self.retrieve_by_panel_id(element_type=element_type, panel_id=panel_id)
        )
        crm_data_serializer = crm_serializer_class(data=new_data, partial=True)
        if crm_data_serializer.is_valid(raise_exception=True):
            crm_serialized_data = crm_data_serializer.validated_data
            return self.update(
                element_type=element_type,
                crm_id=crm_id,
                element_crm_data=element_crm_data,
                **crm_serialized_data,
            )
        return None

    def serialize_and_create(
        self, element_type: ElementType, crm_serializer_class, **data
    ):
        crm_panel_id = data.get("id")
        if crm_id := data.get("crm_id"):
            msg = "{element_type} with CRM ID: {crm_id} already exists!".format(
                element_type=element_type.name, crm_id=crm_id
            )
            raise ValueError(msg)

        if crm_panel_id and self.check_exists(element_type, crm_panel_id):
            msg = "{element_type} with CRM Panel ID: {crm_panel_id} already exists!".format(
                element_type=element_type.name, crm_panel_id=crm_panel_id
            )
            raise ValueError(msg)

        crm_data_serializer = crm_serializer_class(data=data)
        crm_data_serializer.is_valid(raise_exception=True)
        return self.create(
            element_type=element_type, element_data=crm_data_serializer.validated_data
        )

    def check_exists(self, element_type, panel_id):
        element_crm_data = self.retrieve_by_panel_id(
            element_type=element_type, panel_id=panel_id
        )
        return bool(element_crm_data)

    def download_pdf(
        self, crm_id, template_id=settings.DEFAULT_QUOTE_TEMPLATE_ID, language="en"
    ):
        data = {"record": crm_id, "templateid": template_id, "language": language}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.get(
            url=f"{self.base_url}/extended/getpdfmaker",
            data=urlencode(data),
            headers=headers,
            auth=self.authorization_code,
            timeout=5,
        )
        response.raise_for_status()
        name, b64_encoded_data = response.json()["result"]
        decoded_data = base64.b64decode(b64_encoded_data)
        return name, decoded_data


parsvt_crm = ParsVTCRM()
