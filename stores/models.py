from principal.base_models import BaseModel
from users.models import User


from django.db import models

class Region(BaseModel):
    code = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    manager = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='region_manager'
    )

    def __str__(self):
        return self.name

class City(BaseModel):
    code = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities")
    manager = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='city_manager'
    )

    def __str__(self):
        return self.name

class Store(BaseModel):
    code = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="stores"
    )
    address = models.TextField()
    manager = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, related_name='store_manager'
    )

    def __str__(self):
        return self.name
