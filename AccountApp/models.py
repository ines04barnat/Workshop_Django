from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Doctor(User):
    phone = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le numéro de téléphone doit contenir exactement 8 chiffres."
            )
        ]
    )

    licence_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[
            MinLengthValidator(
                6,
                message="Le numéro d'inscription doit contenir exactement 6 caractères."
            )
        ]
    )

    speciality = models.ManyToManyField(
        'Speciality',
        related_name='doctors'
    )


class Patient(models.Model):
    phone = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le numéro de téléphone doit contenir exactement 8 chiffres."
            )
        ]
    )

    birth_date = models.DateField()

    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le CIN doit contenir exactement 8 chiffres."
            )
        ]
    )

    def clean(self):
        super().clean()

        if self.birth_date and self.birth_date >= timezone.localdate():
            raise ValidationError({
                'birth_date': "La date de naissance doit être dans le passé."
            })


class Speciality(models.Model):
    name = models.CharField(max_length=100)