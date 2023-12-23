from django.db import models
import uuid

from principal.base_models import BaseModel


class Rule(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expression = models.TextField()
    formula = models.TextField()

    def __str__(self):
        return f'{self.expression} -> {self.formula}'
