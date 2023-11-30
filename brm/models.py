from django.db import models
import uuid

from principal.base_models import BaseModel


class Rule(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    expression = models.TextField()

    def __str__(self):
        return self.expression