from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Messengers(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    messenger = models.ForeignKey(Messengers, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.email

