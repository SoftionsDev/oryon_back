import uuid

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from brm.models import Rule
from brm.services import ExpressionValidator, FormulaValidator


class RuleReadSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = Rule
        fields = ('id', 'name', 'percentage', 'created_at')


class RuleWriteSerializer(serializers.Serializer):
    name = serializers.CharField()
    rule = serializers.CharField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    formula = serializers.CharField()

    def validate_rule(self, value):
        validator = ExpressionValidator()
        try:
            validator.validate_expression(value)
        except Exception as e:
            raise ValidationError('rule does not compliant the requirements')
        return value.lower()

    def validate_formula(self, value):
        validator = FormulaValidator()
        try:
            validator.validate_expression(value)
        except Exception as e:
            raise ValidationError('formula does not compliant the requirements')
        return value.lower()

    def save(self, **kwargs):
        validated_data = self.validated_data
        rule = Rule.objects.create(
            id=uuid.uuid4(),
            name=validated_data.get('name'),
            expression=validated_data.get('rule'),
            percentage=validated_data.get('percentage'),
            formula=validated_data.get('formula')
        )
        return rule