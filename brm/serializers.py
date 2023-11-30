import uuid

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from brm.models import Rule
from brm.services import ExpressionValidator


class RuleSerializer(serializers.Serializer):
    rule = serializers.CharField()

    def validate_rule(self, value):
        validator = ExpressionValidator()
        try:
            validator.validate_expression(value)
        except Exception as e:
            raise ValidationError('rule does not compliant the requirements')
        return value

    def save(self, **kwargs):
        validated_data = self.validated_data
        rule = Rule.objects.create(
            id=uuid.uuid4(),
            expression=validated_data.get('rule')
        )
        return rule