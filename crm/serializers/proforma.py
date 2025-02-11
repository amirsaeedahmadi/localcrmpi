from rest_framework import serializers
from django.conf import settings
from crm.element_types import ElementTypes
from crm.vtiger import parsvt_crm
from crm.serializers.line_item import LineItemSerializer
from django.urls import reverse


class CRMProformaSerializer(serializers.Serializer):
    id = serializers.CharField(source=settings.CRM_PANEL_PERFORMA_ID_FIELD)
    payable_amount = serializers.DecimalField(
        source="hdnGrandTotal",
        required=False,
        max_digits=25,
        min_value=0,
        decimal_places=10,
    )
    # terms_conditions = serializers.CharField(source="terms_conditions", required=False, allow_blank=True)
    description = serializers.CharField(
        source="comment", required=False, allow_blank=True
    )
    request = serializers.CharField(required=False, allow_blank=True, write_only=True)
    accountable = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )
    ref_code = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
        source=ElementTypes.Proforma.ref_code_field,
    )
    duration = serializers.IntegerField(source=ElementTypes.Proforma.duration_field)
    account_id = serializers.SerializerMethodField()
    potential_id = serializers.SerializerMethodField()
    quotestage = serializers.SerializerMethodField()
    items = LineItemSerializer(many=True)

    class Meta:
        fields = [
            "id",
            "payable_amount",
            "description",
            "request",
            "accountable",
            "ref_code",
            "account_id",
            "potential_id",
            "quotestage",
        ]

    def validate(self, attrs):
        attrs["account_id"] = self.get_account_id(attrs)
        attrs["potential_id"] = self.get_potential_id(attrs)
        attrs.pop("accountable", None)
        attrs.pop("request", None)
        attrs.pop("ref_code", None)
        return attrs

    def to_representation(self, data):
        if hasattr(self, "validated_data"):
            return data
        return super().to_representation(data)

    def validate_payable_amount(self, value):
        # Check if the value is a decimal
        if (
            isinstance(value, float)
            or isinstance(value, str)
            or str(value).split(".")[0].isnumeric()
        ):
            # Convert to Decimal and truncate to remove decimal places
            value = int(
                float(value)
            )  # Convert to float and then to int to discard decimal part
        return value

    def get_account_id(self, value):
        accountable_panel_id = value["accountable"]
        accountable_crm_data = (
            parsvt_crm.retrieve_by_panel_id(
                ElementTypes.Personnel, panel_id=accountable_panel_id
            )
            or {}
        )
        return accountable_crm_data.get("id")

    def get_potential_id(self, value):
        service_request_panel_id = value["request"]
        service_request_crm_data = (
            parsvt_crm.retrieve_by_panel_id(
                ElementTypes.ServiceRequest, panel_id=service_request_panel_id
            )
            or {}
        )
        return service_request_crm_data.get("id")


class ImportCRMProformaSerializer(serializers.Serializer):
    hdnGrandTotal = serializers.DecimalField(
        source="payable_amount",
        required=False,
        max_digits=25,
        min_value=0,
        decimal_places=10,
    )
    # file = serializers.UUIDField(
    #      required=False, allow_blank=True
    # )
    quotestage = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )
    potential_id = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )
    account_id = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )
    # terms_conditions = serializers.CharField(source="description", required=False, allow_blank=True)
    comment = serializers.CharField(
        source="description", required=False, allow_blank=True
    )
    assigned_user_id = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )
    request = serializers.SerializerMethodField()
    accountable = serializers.SerializerMethodField()
    download_link = serializers.SerializerMethodField()
    id = serializers.CharField(source="crm_id")
    # TODO status field and get status should be implemented

    def __init__(self, *args, **kwargs):
        super(ImportCRMProformaSerializer, self).__init__(*args, **kwargs)
        panel_id_field = ElementTypes.Proforma.panel_id_field
        self.fields[panel_id_field] = serializers.CharField(source="id")
        self.fields[ElementTypes.Proforma.ref_code_field] = serializers.CharField(
            source="ref_code", required=False, allow_blank=True
        )
        self.fields[ElementTypes.Proforma.duration_field] = serializers.CharField(
            source="duration", required=False, allow_blank=True
        )

        self.Meta.fields.append(panel_id_field)
        self.Meta.fields.append(ElementTypes.Proforma.ref_code_field)
        self.Meta.fields.append(ElementTypes.Proforma.duration_field)

    class Meta:
        fields = [
            # "file",
            "hdnGrandTotal",
            "request",
            "comment",
            "accountable",
            "account_id",
            "potential_id",
            "quotestage",
            "download_link",
            "assigned_user_id",
        ]

    def validate(self, attrs):
        attrs["request"] = self.get_request(attrs)
        attrs["accountable"] = self.get_accountable(attrs)
        attrs["download_link"] = self.get_download_link(attrs)
        if not attrs.get("description"):
            attrs.pop("description", None)
        return attrs

    def to_representation(self, data):
        if hasattr(self, "validated_data"):
            return data
        return super().to_representation(data)

    def get_request(self, value):
        potential_id = value["potential_id"]
        potential_crm_data = parsvt_crm.retrieve(
            ElementTypes.ServiceRequest, crm_id=potential_id
        )
        if potential_crm_data:
            return potential_crm_data[0][ElementTypes.ServiceRequest.panel_id_field]
        return None

    def get_accountable(self, value):
        personnel_id = value["assigned_user_id"]
        personnel_crm_data = parsvt_crm.retrieve(
            ElementTypes.Personnel, crm_id=personnel_id
        )
        if personnel_crm_data:
            return personnel_crm_data[0][ElementTypes.Personnel.panel_id_field]
        return None

    def get_download_link(self, value):
        proforma_crm_id = value["crm_id"]
        return reverse("proforma_file_download_by_crm_id", args=[proforma_crm_id])

    def validate_hdnGrandTotal(self, value):
        if (
            isinstance(value, float)
            or isinstance(value, str)
            or str(value).split(".")[0].isnumeric()
        ):
            value = int(float(value))
        return value
