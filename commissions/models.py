from django.db import models

from brm.models import Rule
from principal.base_models import BaseModel
from sales.models import Sale
from users.models import User


class Commission(BaseModel):
    id = models.UUIDField(primary_key=True)
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    rule = models.ForeignKey(Rule, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"Commission {self.id}"
