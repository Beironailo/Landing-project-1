from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Messengers(models.Model):
    """Доступные мессенджеры"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мессенджер'
        verbose_name_plural = 'Мессенджеры'


class Profile(models.Model):
    """Пользователи"""
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    messenger = models.ForeignKey(Messengers, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
