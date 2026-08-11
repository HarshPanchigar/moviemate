from django.db import models


class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name