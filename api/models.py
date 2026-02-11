from django.db import models

class MissingPerson(models.Model):  
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('MISSING', 'Missing'),
        ('FOUND', 'Found'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    age = models.IntegerField(null=True, blank=True, verbose_name="Age")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male', verbose_name="Gender")
    
    last_seen_date = models.DateTimeField(verbose_name="Last Seen Date", null=True, blank=True)
    last_seen_location = models.TextField(verbose_name="Last Seen Location")
    
    description = models.TextField(null=True, blank=True, verbose_name="Physical Description")
    contact_phone = models.CharField(max_length=20, verbose_name="Contact Phone")
    
    image = models.ImageField(upload_to='missing_persons/', null=True, blank=True, verbose_name="Person Image")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='MISSING', verbose_name="Status")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
