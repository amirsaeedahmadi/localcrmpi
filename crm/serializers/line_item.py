from rest_framework import serializers


class LineItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    productid = serializers.CharField(source="hdnProductId")
    comment = serializers.CharField()
    listprice = serializers.CharField(
        source="listPrice",
        allow_blank=True,
    )
    discount_amount = serializers.CharField(allow_blank=True, allow_null=True)
    quantity = serializers.CharField(
        source="qty",
        allow_blank=True,
        required=False,
    )
    tax1 = serializers.CharField(
        source="tax1_percentage", allow_blank=True, required=False, allow_null=True
    )
    tax2 = serializers.CharField(
        source="tax2_percentage", allow_blank=True, required=False, allow_null=True
    )
    tax3 = serializers.CharField(
        source="tax3_percentage", allow_blank=True, required=False, allow_null=True
    )

    class Meta:
        fields = [
            "id",
            "productid",
            "quantity",
            "listprice",
            "comment",
            "discount_amount",
            "tax1",
            "tax2",
            "tax3",
        ]

    def decimal_to_int(self, value):
        if (
            isinstance(value, float)
            or isinstance(value, str)
            or str(value).split(".")[0].isnumeric()
        ) and str(value):
            value = int(float(value))
        return value

    def validate_quantity(self, value):
        return self.decimal_to_int(value)

    def validate_listprice(self, value):
        return self.decimal_to_int(value)

    def validate_discount_amount(self, value):
        return self.decimal_to_int(value)

    def validate_tax1(self, value):
        return self.decimal_to_int(value)

    def validate_tax2(self, value):
        return self.decimal_to_int(value)

    def validate_tax3(self, value):
        return self.decimal_to_int(value)
