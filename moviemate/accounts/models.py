from django.db import models


class Customer(models.Model):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('admin', 'Admin'),
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return f"{self.full_name} ({self.role})"