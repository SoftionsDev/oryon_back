from django.db import models

from principal.base_models import BaseModel
from stores.models import Store
from products.models import Product
from users.models import User


class Sale(BaseModel):
    id = models.UUIDField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    commercial = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField()
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Sale {self.id}"
