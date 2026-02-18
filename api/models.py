from django.db import models
from django.utils import timezone

class MissingPerson(models.Model):
    STATUS_CHOICES = [
        ('MISSING', 'Missing'),
        ('FOUND', 'Found'),
    ]

    full_name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    last_seen_date = models.DateTimeField(default=timezone.now)
    last_seen_location = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='MISSING')
    description = models.TextField(blank=True, null=True)
    clothing_description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='missing_persons/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
