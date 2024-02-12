from django.db import models
import uuid

from principal.base_models import BaseModel


class Rule(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
<<<<<<< Updated upstream
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expression = models.TextField()
    formula = models.TextField()
=======

    def __str__(self):
        return f"{self.name} -> {self.rule}"

    @property
    def available_percentages(self) -> list:
        return [
            self.director,
            self.manager,
            self.commercial,
            self.assistant
        ]

    @property
    def has_formula(self):
        return self.formula is not None


class Formula(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    formula = models.TextField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    rule = models.OneToOneField(
        Percentages, on_delete=models.CASCADE, related_name='formula'
    )
>>>>>>> Stashed changes

    def __str__(self):
        return f'{self.expression} -> {self.formula}'
