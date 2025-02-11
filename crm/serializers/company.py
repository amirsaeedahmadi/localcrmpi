from rest_framework import serializers
from django.conf import settings
from crm.element_types import ElementTypes
from crm.vtiger import parsvt_crm


class CRMCompanySerializer(serializers.Serializer):
    id = serializers.CharField(source=settings.CRM_PANEL_COMPANY_ID_FIELD)
    user = serializers.UUIDField()
    name = serializers.CharField(source="accountname", required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(source="email1", required=False, allow_blank=True)
    national_code = serializers.CharField(
        source="cf_pcf_lid_1036", required=False, allow_blank=True
    )
    economical_number = serializers.CharField(
        source="cf_pcf_irv_1034", required=False, allow_blank=True
    )
    postal_code = serializers.CharField(
        source="ship_code", required=False, allow_blank=True
    )
    postal_address = serializers.CharField(
        source="bill_street", required=False, allow_blank=True
    )
    ownership = serializers.SerializerMethodField(
        allow_null=True,
    )

    class Meta:
        fields = [
            "id" "name",
            "phone",
            "email",
            "postal_code",
            "postal_address",
            "national_code",
            "economical_number",
            "ownership",
        ]

    def get_ownership(self, value):
        if user_id := value.get("user"):
            owner_crm_data = parsvt_crm.retrieve_by_panel_id(
                ElementTypes.User, panel_id=user_id
            )
            return f"{owner_crm_data.get('firstname')} {owner_crm_data.get('lastname')}"
        return ""

    def validate(self, attrs):
        attrs["ownership"] = self.get_ownership(attrs)
        attrs.pop("user", None)
        return attrs

    def to_representation(self, data):
        if hasattr(self, "validated_data"):
            return data
        return super().to_representation(data)


class ImportCRMCompanySerializer(serializers.ModelSerializer):
    accountname = serializers.CharField(source="name", required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    email1 = serializers.EmailField(source="email", required=False, allow_blank=True)
    cf_pcf_lid_1036 = serializers.CharField(
        source="national_code", required=False, allow_blank=True
    )
    cf_pcf_irv_1034 = serializers.CharField(
        source="economical_number", required=False, allow_blank=True
    )
    ship_code = serializers.CharField(
        source="postal_code", required=False, allow_blank=True
    )
    ship_street = serializers.CharField(
        source="postal_address", allow_blank=True, default=""
    )

    def __init__(self, *args, **kwargs):
        super(ImportCRMCompanySerializer, self).__init__(*args, **kwargs)
        panel_id_field = ElementTypes.Company.panel_id_field
        self.fields[panel_id_field] = serializers.CharField(source="id")
        self.Meta.fields.append(panel_id_field)

    class Meta:
        fields = [
            "accountname",
            "phone",
            "email1",
            "cf_pcf_lid_1036",
            "cf_pcf_irv_1034",
            "ship_code",
            "ship_street",
        ]
