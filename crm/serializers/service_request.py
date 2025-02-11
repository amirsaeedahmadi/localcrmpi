from rest_framework import serializers
from django.conf import settings
from crm.element_types import ElementTypes
from crm.vtiger import parsvt_crm
from crm.serializers.user import UserSerializer, ImportCRMUserSerializer
from datetime import datetime, timedelta
from .enum import CRMSalesStageChoices, PanelServiceRequestStatusChoices


class CRMServiceRequestDescriptionSerializer(serializers.Serializer):
    dr_solution = serializers.BooleanField(required=False)
    main_site = serializers.BooleanField(required=False)
    multi_site = serializers.BooleanField(required=False)
    on_premise = serializers.BooleanField(required=False)
    container_count = serializers.IntegerField(required=False)
    microservice_count = serializers.IntegerField(required=False)
    advanced_data_backup = serializers.BooleanField(required=False)
    high_load_db_count = serializers.IntegerField(required=False)
    normal_load_db_count = serializers.IntegerField(required=False)
    high_load_oracle_count = serializers.IntegerField(required=False)
    normal_load_oracle_count = serializers.IntegerField(required=False)
    high_load_oracle_cluster_count = serializers.IntegerField(required=False)
    normal_load_oracle_cluster_count = serializers.IntegerField(required=False)
    nosql_db_count = serializers.IntegerField(required=False)
    big_data_count = serializers.IntegerField(required=False)
    object_storage_count = serializers.IntegerField(required=False)
    ng_firewall = serializers.BooleanField(required=False)
    ng_waf = serializers.BooleanField(required=False)
    advanced_security = serializers.BooleanField(required=False)
    load_balancer = serializers.BooleanField(required=False)
    advanced_monitoring = serializers.BooleanField(required=False)
    log_management = serializers.BooleanField(required=False)
    siem = serializers.BooleanField(required=False)
    migration = serializers.BooleanField(required=False)
    devops_adoption = serializers.BooleanField(required=False)
    daas = serializers.BooleanField(required=False)
    db_management = serializers.BooleanField(required=False)
    data_platform_management = serializers.BooleanField(required=False)
    os_management = serializers.BooleanField(required=False)
    microservice_management = serializers.BooleanField(required=False)
    security = serializers.BooleanField(required=False)
    description = serializers.SerializerMethodField(required=False)
    description_fields = [
        "dr_solution",
        "main_site",
        "multi_site",
        "on_premise",
        "container_count",
        "microservice_count",
        "advanced_data_backup",
        "high_load_db_count",
        "normal_load_db_count",
        "high_load_oracle_count",
        "normal_load_oracle_count",
        "high_load_oracle_cluster_count",
        "normal_load_oracle_cluster_count",
        "nosql_db_count",
        "big_data_count",
        "object_storage_count",
        "ng_firewall",
        "ng_waf",
        "advanced_security",
        "load_balancer",
        "advanced_monitoring",
        "log_management",
        "siem",
        "migration",
        "devops_adoption",
        "daas",
        "db_management",
        "data_platform_management",
        "os_management",
        "microservice_management",
        "security",
    ]

    def get_description(self, attrs):
        description, i = "", 1
        for key in self.description_fields:
            if ex_attr := attrs.get(key):
                description += f"{i}. {key}: {ex_attr}\n"
                i += 1
            attrs.pop(key, None)
        attrs["description"] = description
        return description

    def validate(self, attrs):
        attrs["description"] = self.get_description(attrs)
        for key in self.description_fields:
            attrs.pop(key, None)
        return attrs

    def to_representation(self, data):
        if hasattr(self, "validated_data"):
            return data
        return super().to_representation(data)


class CRMServiceRequestSerializer(CRMServiceRequestDescriptionSerializer):
    id = serializers.CharField(source=settings.CRM_PANEL_SERVICE_REQUEST_ID_FIELD)
    user = UserSerializer(write_only=True)
    ref_code = serializers.CharField(required=False)
    status = serializers.IntegerField(required=False)
    related_to = serializers.SerializerMethodField(read_only=True)
    contact_id = serializers.SerializerMethodField()
    sales_stage = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()
    potentialname = serializers.SerializerMethodField()

    class Meta:
        fields = [
            "id" "user",
            "ref_code",
            "status",
            "description",
            "related_to",
            "contact_id",
            "sales_stage",
            "closingdate",
            "potentialname",
        ]

    def get_related_to(self, value):
        user_panel_id = value["user"]["id"]
        user_crm_data = (
            parsvt_crm.retrieve_by_panel_id(ElementTypes.User, panel_id=user_panel_id)
            or {}
        )
        return user_crm_data.get("account_id")

    def get_contact_id(self, value):
        user_panel_id = value["user"]["id"]
        user_crm_data = (
            parsvt_crm.retrieve_by_panel_id(ElementTypes.User, panel_id=user_panel_id)
            or {}
        )
        return user_crm_data.get("id")

    def get_sales_stage(self, value):
        return CRMSalesStageChoices.Needs_Analysis

    def get_closing_date(self, value):
        return (datetime.now() + timedelta(days=365)).strftime(
            "%Y-%m-%d"
        )  # TODO read from .env

    def get_potentialname(self, value):
        first_name = (
            value["user"]["first_name"]
            if value.get("user", {}).get("first_name")
            else ""
        )
        last_name = (
            value["user"]["last_name"] if value.get("user", {}).get("last_name") else ""
        )
        potential_name = " ".join(
            [first_name, last_name, datetime.now().strftime("%Y-%m-%d")]
        )
        return potential_name

    def validate(self, attrs):
        attrs = super(CRMServiceRequestSerializer, self).validate(attrs)
        attrs["related_to"] = self.get_related_to(attrs)
        attrs["contact_id"] = self.get_contact_id(attrs)
        attrs["closingdate"] = self.get_closing_date(attrs)
        attrs["potentialname"] = self.get_potentialname(attrs)
        attrs["sales_stage"] = self.get_sales_stage(attrs)
        attrs.pop("ref_code", None)
        attrs.pop("status", None)
        attrs.pop("user", None)
        return attrs

    def to_representation(self, data):
        if hasattr(self, "validated_data"):
            return data
        return super().to_representation(data)


class ImportCRMServiceRequestSerializer(serializers.Serializer):
    related_to = serializers.CharField(required=False, allow_blank=True)
    contact_id = serializers.CharField(required=False, allow_blank=True)
    closingdate = serializers.CharField(required=False, allow_blank=True)
    potentialname = serializers.CharField(required=False, allow_blank=True)
    sales_stage = serializers.ChoiceField(choices=CRMSalesStageChoices.choices)
    ref_code = serializers.SerializerMethodField()
    status = serializers.ChoiceField(
        required=False,
        allow_blank=True,
        choices=PanelServiceRequestStatusChoices.choices,
    )
    user = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(ImportCRMServiceRequestSerializer, self).__init__(*args, **kwargs)
        panel_id_field = ElementTypes.ServiceRequest.panel_id_field
        self.fields[panel_id_field] = serializers.CharField(source="id")
        self.Meta.fields.append(panel_id_field)

    class Meta:
        fields = [
            "related_to",
            "contact_id",
            "closingdate",
            "potentialname",
            "sales_stage",
            "ref_code",
            "status",
            "user",
        ]

    def validate(self, attrs):
        if attrs.get("contact_id"):
            attrs["user"] = self.get_user(attrs)
        attrs.pop("related_to", None)
        attrs.pop("contact_id", None)
        attrs.pop("closingdate", None)
        attrs.pop("sales_stage", None)
        attrs.pop("ref_code", None)
        return attrs

    def to_representation(self, data):
        if hasattr(self, "validated_data"):
            return data
        return super().to_representation(data)

    def get_user(self, value):
        if contact_id := value.get("contact_id"):
            if contact_info := parsvt_crm.retrieve(
                ElementTypes.User, crm_id=contact_id
            ):
                contact_info = contact_info[0]
                user_serializer = ImportCRMUserSerializer(data=contact_info)
                user_serializer.is_valid(raise_exception=True)
                return user_serializer.validated_data
        return None
