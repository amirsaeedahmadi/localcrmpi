from rest_framework import serializers
from crm.element_types import ElementTypes


class CRMUserSerializer(serializers.Serializer):
    id = serializers.CharField(source=ElementTypes.User.panel_id_field)
    first_name = serializers.CharField(
        source="firstname", required=False, allow_blank=True
    )
    last_name = serializers.CharField(
        source="lastname", required=False, allow_blank=True
    )
    email = serializers.EmailField(required=False, allow_blank=True)
    postal_code = serializers.CharField(
        source="mailingzip", required=False, allow_blank=True
    )
    national_code = serializers.CharField(
        source="cf_pcf_irc_1124", required=False, allow_blank=True
    )
    mobile = serializers.CharField(required=False, allow_blank=True)
    postal_address = serializers.CharField(
        source="mailingstreet", default="", allow_blank=True
    )
    account_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "postal_address",
            "postal_code",
            "national_code",
            "account_id",
        ]


class ImportCRMUserSerializer(serializers.Serializer):
    firstname = serializers.CharField(
        source="first_name", required=False, allow_blank=True
    )
    lastname = serializers.CharField(
        source="last_name", required=False, allow_blank=True
    )
    email = serializers.EmailField(required=False, allow_blank=True)
    mailingzip = serializers.CharField(
        source="postal_code", required=False, allow_blank=True
    )
    cf_pcf_irc_1124 = serializers.CharField(
        source="national_code", required=False, allow_blank=True
    )
    mobile = serializers.CharField(required=False, allow_blank=True)
    mailingstreet = serializers.CharField(
        source="postal_address", default="", allow_blank=True
    )
    account_id = serializers.CharField(required=False, allow_blank=True)

    def __init__(self, *args, **kwargs):
        super(ImportCRMUserSerializer, self).__init__(*args, **kwargs)
        panel_id_field = ElementTypes.User.panel_id_field
        self.fields[panel_id_field] = serializers.CharField(source="id")
        self.Meta.fields.append(panel_id_field)

    class Meta:
        fields = [
            "firstname",
            "lastname",
            "email",
            "mobile",
            "mailingstreet",
            "mailingzip",
            "cf_pcf_irc_1124",
            "account_id",
        ]

    def validate(self, attrs):
        attrs.pop("account_id")
        return attrs

    def to_representation(self, data):
        if hasattr(self, "validated_data"):
            return data
        return super().to_representation(data)


class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True)
    national_code = serializers.CharField(required=False, allow_blank=True)
    mobile = serializers.CharField(required=False, allow_blank=True)
    postal_address = serializers.CharField(default="", allow_blank=True)

    class Meta:
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "postal_address",
            "postal_code",
            "national_code",
        ]
