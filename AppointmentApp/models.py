from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Status(models.TextChoices):
    Pending = 'Pending', 'Pending'
    Confirmed = 'Confirmed', 'Confirmed'
    Cancelled = 'Cancelled', 'Cancelled'


class Appointment(models.Model):
    reason = models.TextField()

    duration_minutes = models.DurationField()

    appointment_date = models.DateTimeField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf'],
                message="L'ordonnance doit être un fichier PDF."
            )
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        choices=Status.choices,
        max_length=10,
        default=Status.Pending
    )

    doctor = models.ForeignKey(
        "AccountApp.Doctor",
        on_delete=models.CASCADE,
        null=True
    )

    patient = models.ForeignKey(
        "AccountApp.Patient",
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_datetime'
            )
        ]

    def clean(self):
        super().clean()

        if self.appointment_date and self.appointment_date <= timezone.now():
            raise ValidationError({
                'appointment_date':
                    "La date et l'heure du rendez-vous doivent être dans le futur."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)