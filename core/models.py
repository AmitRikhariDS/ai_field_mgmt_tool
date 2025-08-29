from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import date
User = get_user_model()
# class Client(models.Model):
#     name = models.CharField(max_length=255)
#     contact_email = models.EmailField(blank=True, null=True)
#     contact_phone = models.CharField(max_length=30, blank=True, null=True)
#     def __str__(self):
#         return self.name
    

# api/models.py
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name


from django.db import models
# from django.utils.timezone import now

# class Engineer(models.Model):
#     # ... other fields ...

    

#     def save(self, *args, **kwargs):
#         self.updated_at = now()  # update timestamp on each save
#         super().save(*args, **kwargs)

from django.db import models
from django.utils.timezone import now

class Engineer(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')

    certifications = models.TextField(blank=True)
    education = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    image = models.ImageField(upload_to='engineers/', blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    primary_skills = models.TextField(blank=True)
    summary = models.TextField(blank=True)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Job(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    job_code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    engineer = models.ForeignKey(Engineer, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    priority = models.CharField(max_length=20, default="medium")
    scheduled_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.job_code} - {self.title}"
# models.py (already defined)
class TimeEntry(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    @property
    def hours_worked(self):
        if self.end:
            return (self.end - self.start).total_seconds() / 3600
        return 0


from datetime import date, datetime

class Invoice(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    engineer = models.ForeignKey('Engineer', on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey('Job', on_delete=models.SET_NULL, null=True, blank=True)

    invoice_number = models.CharField(max_length=20, unique=True, default="INV-DEFAULT")
    date = models.DateField(default=date.today)               # Invoice date
    created_at = models.DateTimeField(default=datetime.now)   # Timestamp for DB ordering
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    per_hour_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")  # Pending, Generated, Paid

    def save(self, *args, **kwargs):
    # Calculate total based on hours_worked * per_hour_charge
        if not self.total_amount:
            self.total_amount = self.hours_worked * self.per_hour_charge

        # Generate unique invoice number if not present
        if not self.invoice_number:
            from datetime import datetime
            import random
            self.invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"

        super().save(*args, **kwargs)



