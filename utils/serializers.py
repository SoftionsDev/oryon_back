import re
from rest_framework import serializers


class CustomDecimalField(serializers.DecimalField):
    def to_internal_value(self, data):
        cleaned_data = re.sub(r"[\s.,]+", '', data)
        return super().to_internal_value(cleaned_data)

class SelectableFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        context = kwargs.get('context', {})
        fields = context.get('fields')

        # Dynamically modify the fields to serialize
        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)