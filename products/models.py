from django.db import models

from principal.base_models import BaseModel


class Product(BaseModel):
    code = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=255)
    category_description = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    brand_description = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} / {self.price}'
