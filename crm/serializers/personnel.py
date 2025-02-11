from rest_framework import serializers
from crm.element_types import ElementTypes


class ImportCRMPersonnelSerializer(serializers.Serializer):
    id = serializers.CharField(source="crm_id")
    user_name = serializers.CharField(
        source="username", required=False, allow_blank=True
    )
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    user_password = serializers.CharField(
        source="password", required=False, allow_blank=True
    )
    email1 = serializers.EmailField(source="email", required=False, allow_blank=True)
    phone_mobile = serializers.CharField(
        source="mobile", required=False, allow_blank=True
    )

    is_crm_personnel = serializers.BooleanField(default=True)
    is_admin = serializers.CharField(write_only=True)
    is_crm_admin = serializers.SerializerMethodField()
    email_verified = serializers.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super(ImportCRMPersonnelSerializer, self).__init__(*args, **kwargs)
        panel_id_field = ElementTypes.Personnel.panel_id_field
        self.fields[panel_id_field] = serializers.CharField(
            source="id", required=False, allow_blank=True
        )
        self.Meta.fields.append(panel_id_field)

    def get_is_crm_admin(self, value):
        is_admin = value["is_admin"]
        return True if is_admin == "on" else False

    def validate(self, attrs):
        attrs["is_crm_admin"] = self.get_is_crm_admin(attrs)
        attrs.pop("is_admin", None)
        return attrs

    def to_representation(self, data):
        if hasattr(self, "validated_data"):
            return data
        return super().to_representation(data)

    class Meta:
        fields = [
            "id",
            "user_name",
            "first_name",
            "last_name",
            "user_password",
            "email1",
            "phone_mobile",
            "panelid",
            "is_crm_personnel",
            "is_crm_admin",
            "email_verified",
        ]


class CRMPersonnelSerializer(serializers.Serializer):
    username = serializers.CharField(
        source="user_name", required=False, allow_blank=True
    )
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(
        source="user_password", required=False, allow_blank=True
    )
    email = serializers.EmailField(source="email1", required=False, allow_blank=True)
    mobile = serializers.CharField(
        source="phone_mobile", required=False, allow_blank=True
    )
    id = serializers.UUIDField(source=ElementTypes.Personnel.panel_id_field)
    is_crm_admin = serializers.BooleanField(source="is_admin", default=False)

    class Meta:
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "mobile",
            "id",
            "is_crm_admin",
        ]
