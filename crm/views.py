from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.http import FileResponse
from crm.vtiger import parsvt_crm
from crm.element_types import ElementTypes
from crm.services import personnel_service, proforma_service, service_request_service
from io import BytesIO
from uuid import uuid4


class ProformaFileDownloadView(ViewSet):
    # permission_classes = [IsAuthenticated]

    def download_by_crm_id(self, request, crm_id):
        proforma_crm_data = parsvt_crm.retrieve(
            element_type=ElementTypes.Proforma, crm_id=crm_id
        )
        if proforma_crm_data:
            filename, proforma_file_data = parsvt_crm.download_pdf(crm_id=crm_id)
            return FileResponse(
                BytesIO(proforma_file_data), as_attachment=True, filename=filename
            )
        return Response(
            data={"error": "File not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def download_by_panel_id(self, request, proforma_panel_id):
        proforma_crm_data = parsvt_crm.retrieve_by_panel_id(
            element_type=ElementTypes.Proforma, panel_id=proforma_panel_id
        )
        if proforma_crm_data:
            filename, proforma_file_data = parsvt_crm.download_pdf(
                crm_id=proforma_crm_data["id"]
            )
            return FileResponse(
                BytesIO(proforma_file_data), as_attachment=True, filename=filename
            )
        return Response(
            data={"error": "File not found"}, status=status.HTTP_404_NOT_FOUND
        )


class ProformaCreationHookView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, crm_id):
        try:
            panel_id = str(uuid4())
            proforma_crm_data = parsvt_crm.retrieve(
                ElementTypes.Proforma, crm_id=crm_id
            )
            if not proforma_crm_data:
                return Response(
                    data={"status": False, "message": "Proforma Not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            proforma_crm_data = proforma_crm_data[0]
            proforma_crm_data[ElementTypes.Proforma.panel_id_field] = panel_id
            proforma_service.on_proforma_created(**proforma_crm_data)
            return Response(
                data={
                    "status": True,
                    "message": "Proforma creation published successfully",
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            return Response(
                data={
                    "status": False,
                    "message": f"Proforma creation publish failed\n {e}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class PersonnelCreationHookView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, crm_id):
        personnel_crm_data = parsvt_crm.retrieve(ElementTypes.Personnel, crm_id=crm_id)
        if not personnel_crm_data:
            return Response(
                data={"status": False, "message": "Proforma Not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        personnel_crm_data = personnel_crm_data[0]
        panel_id = str(uuid4())
        old_panel_id = personnel_crm_data.get(ElementTypes.Personnel.panel_id_field)
        personnel_crm_data[ElementTypes.Personnel.panel_id_field] = old_panel_id or str(
            panel_id
        )
        personnel_service.on_personnel_created(**personnel_crm_data)
        return Response(
            data={
                "status": True,
                "message": "Personnel creation published successfully",
            },
            status=status.HTTP_200_OK,
        )


class ServiceRequestUpdateHook(ViewSet):
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "update_status":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def update_status(self, request, new_status, crm_id):
        if new_status == "inspect":
            return self._update_status_to_inspecting(request, crm_id)
        return Response(
            data={"status": False, "message": "Invalid status"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _retrieve_service_request(self, crm_id):
        service_request_crm_data = parsvt_crm.retrieve(
            ElementTypes.ServiceRequest, crm_id=crm_id
        )
        if not service_request_crm_data:
            return Response(
                data={"status": False, "message": "Service Request Not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        service_request_crm_data = service_request_crm_data[0]
        return service_request_crm_data

    def _update_status_to_inspecting(self, request, crm_id):
        service_request_crm_data = self._retrieve_service_request(crm_id)
        service_request_service.on_inspected(**service_request_crm_data)
        return Response(
            data={
                "status": True,
                "message": "Service Request status update published successfully",
            },
            status=status.HTTP_200_OK,
        )
