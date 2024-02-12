import logging
import uuid

from django.db import DatabaseError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from brm.models import Percentages, Formula
from brm.services import FormulaValidator, RuleValidator

logger = logging.getLogger(__name__)


class PercentagesReadSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format='%Y-%m-%d')
    has_formula = serializers.BooleanField()

    class Meta:
        model = Percentages
        exclude = ('updated_at',)


class PercentagesWriteSerializer(serializers.Serializer):
    name = serializers.CharField()
    rule = serializers.CharField()
    director = serializers.DecimalField(max_digits=5, decimal_places=2)
    manager = serializers.DecimalField(max_digits=5, decimal_places=2)
    commercial = serializers.DecimalField(max_digits=5, decimal_places=2)
    assistant = serializers.DecimalField(max_digits=5, decimal_places=2)

    def validate_rule(self, value):
        validator = RuleValidator()
        try:
            validator.validate_expression(value)
        except Exception as e:
            logger.exception(e)
            raise ValidationError('rule does not compliant the requirements')
        return value.lower()

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

    def validate_formula(self, value):
        validator = FormulaValidator()
        try:
            validator.validate_expression(value)
        except Exception as e:
            raise ValidationError('formula does not compliant the requirements')
        return value.lower()

    def save(self, **kwargs):
        # this is a relation to table percentage to its rule
        percentage = Percentages.objects.filter(
            id=self.validated_data.get('rule')
        ).first()
        if not percentage:
            raise ValidationError('The percentage does not exist')
        if self.validated_data.get('percentage') not in percentage.available_percentages:
            raise ValidationError('Inconsistent Percentage')

        try:
            formula = Formula.objects.create(
                id=uuid.uuid4(),
                formula=self.validated_data.get('formula'),
                percentage=self.validated_data.get('percentage'),
                rule=percentage
            )
            return formula
        except DatabaseError as e:
            logger.exception(e)
            raise ValidationError('An error has occurred while saving the formula')