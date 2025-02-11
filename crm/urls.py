from django.urls import path
from .views import (
    ProformaFileDownloadView,
    ProformaCreationHookView,
    PersonnelCreationHookView,
    ServiceRequestUpdateHook,
)

urlpatterns = [
    path(
        "download_by_panel_id/<str:proforma_panel_id>",
        ProformaFileDownloadView.as_view({"get": "download_by_panel_id"}),
        name="proforma_file_download_by_panel_id",
    ),
    path(
        "download_by_crm_id/<str:crm_id>",
        ProformaFileDownloadView.as_view({"get": "download_by_crm_id"}),
        name="proforma_file_download_by_crm_id",
    ),
    path(
        "proforma_creation_hook/<str:crm_id>",
        ProformaCreationHookView.as_view(),
        name="proforma_creation_hook",
    ),
    path(
        "personnel_creation_hook/<str:crm_id>",
        PersonnelCreationHookView.as_view(),
        name="personnel_creation_hook",
    ),
    path(
        "service_request_update_status/<str:new_status>/<str:crm_id>",
        ServiceRequestUpdateHook.as_view({"post": "update_status"}),
        name="service_request_update_status",
    ),
]
