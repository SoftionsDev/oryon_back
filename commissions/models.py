from django.db import models

from principal.base_models import BaseModel
from sales.models import Sale

class Commission(BaseModel):
    id = models.UUIDField(primary_key=True)
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Commission {self.id}"
