from django.db import models
import uuid

from principal.base_models import BaseModel


class Percentages(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    rule = models.TextField()
    director = models.DecimalField(max_digits=5, decimal_places=2)
    manager = models.DecimalField(max_digits=5, decimal_places=2)
    commercial = models.DecimalField(max_digits=5, decimal_places=2)
    assistant = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

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


class Formula(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    formula = models.TextField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    rule = models.OneToOneField(
        Percentages, on_delete=models.DO_NOTHING, related_name='formula'
    )

    def __str__(self):
        return f'{self.rule.name} -> {self.formula}'
