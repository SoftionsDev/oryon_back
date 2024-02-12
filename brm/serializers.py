import uuid

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from brm.models import Rule
from brm.services import ExpressionValidator, FormulaValidator


class RuleReadSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format='%Y-%m-%d')
    has_formula = serializers.BooleanField()

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
            logger.exception(e)
            raise ValidationError('rule does not compliant the requirements')
        return value.lower()

<<<<<<< Updated upstream
=======
    def validate(self, data):
        decimal_fields = ['director', 'manager', 'commercial', 'assistant']
        for field in decimal_fields:
            if data.get(field) == 0:
                raise ValidationError(f"{field} cannot be 0.")
        return data

    def save(self, **kwargs):
        try:
            percentage = Percentages.objects.create(
                id=uuid.uuid4(),
                name=self.validated_data.get('name'),
                rule=self.validated_data.get('rule'),
                manager=self.validated_data.get('manager'),
                director=self.validated_data.get('director'),
                commercial=self.validated_data.get('commercial'),
                assistant=self.validated_data.get('assistant')
            )
            return percentage
        except DatabaseError as e:
            logger.exception(e)
            raise ValidationError('An error has occurred while saving the percentage')


class FormulaReadSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format='%Y-%m-%d')
    name = serializers.CharField(source='rule.name')
    rule = serializers.CharField(source='rule.rule')

    class Meta:
        model = Formula
        exclude = ('updated_at',)


class FormulaWriteSerializer(serializers.Serializer):
    formula = serializers.CharField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    rule = serializers.CharField()

>>>>>>> Stashed changes
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