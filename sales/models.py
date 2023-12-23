from django.db import models

from principal.base_models import BaseModel
from sales.constants import SalesTypes, CommissionTypes
from stores.models import Store
from products.models import Product
from users.models import User


class Sale(BaseModel):

    SALES_TYPES_CHOICES = [(tag.name, tag.value) for tag in SalesTypes]
    COMMISSION_TYPES_CHOICES = [(tag.name, tag.value) for tag in CommissionTypes]

    id = models.UUIDField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField()
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    type_ = models.CharField(
        max_length=100, name='type',
        choices=SALES_TYPES_CHOICES,
        default=SalesTypes.SELF.value
    )
    commission_type = models.CharField(
        max_length=100,
        choices=COMMISSION_TYPES_CHOICES,
        default=CommissionTypes.SALE.value
    )
    commissioned = models.BooleanField(default=False)

    def __str__(self):
        return f"Sale {self.id}"
