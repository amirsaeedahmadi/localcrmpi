from django.conf import settings


class ElementType:
    name = None
    panel_id_field = None
    is_inventory_model = False

    def __str__(self):
        return self.name


class User(ElementType):
    name = "Contacts"
    panel_id_field = settings.CRM_PANEL_USER_ID_FIELD


class Company(ElementType):
    name = "Accounts"
    panel_id_field = settings.CRM_PANEL_COMPANY_ID_FIELD


class Proforma(ElementType):
    name = "Quotes"
    is_inventory_model = True
    panel_id_field = settings.CRM_PANEL_PERFORMA_ID_FIELD
    ref_code_field = settings.CRM_PANEL_PERFORMA_REF_CODE_FIELD
    duration_field = settings.CRM_PANEL_PERFORMA_DURATION_FIELD


class ServiceRequest(ElementType):
    name = "Potentials"
    panel_id_field = settings.CRM_PANEL_SERVICE_REQUEST_ID_FIELD


class Personnel(ElementType):
    name = "Users"
    panel_id_field = settings.CRM_PERSONNEL_ID_FIELD


class LineItem(ElementType):
    name = "LineItem"
    panel_id_field = None


class ElementTypes:
    User = User
    Company = Company
    Proforma = Proforma
    ServiceRequest = ServiceRequest
    Personnel = Personnel
    LineItem = LineItem
