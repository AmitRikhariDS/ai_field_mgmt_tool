from django.contrib import admin
from .models import Client, Engineer, Job, TimeEntry, Invoice
admin.site.register(Client)
admin.site.register(Engineer)
admin.site.register(Job)
admin.site.register(TimeEntry)
admin.site.register(Invoice)
