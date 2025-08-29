# core/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Job, Engineer, Client, Invoice

class Command(BaseCommand):
    help = "Create default user groups and permissions"

    def handle(self, *args, **kwargs):
        groups = ["Field Engineer", "PMO", "Client", "Account Team", "Admin"]
        for g in groups:
            group, created = Group.objects.get_or_create(name=g)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Group '{g}' created"))

        # Assign permissions
        # PMO and Admin -> all permissions
        all_perms = Permission.objects.all()
        for g in ["PMO", "Admin"]:
            group = Group.objects.get(name=g)
            group.permissions.set(all_perms)

        # Account Team -> invoice & reports
        account_group = Group.objects.get(name="Account Team")
        invoice_ct = ContentType.objects.get_for_model(Invoice)
        invoice_perms = Permission.objects.filter(content_type=invoice_ct)
        # you can also add report permissions if you have a Report model
        account_group.permissions.set(invoice_perms)

        # Field Engineer -> job view & update only for assigned jobs
        engineer_group = Group.objects.get(name="Field Engineer")
        job_ct = ContentType.objects.get_for_model(Job)
        # give view & change permissions
        job_perms = Permission.objects.filter(content_type=job_ct).filter(codename__in=["view_job","change_job"])
        engineer_group.permissions.set(job_perms)

        self.stdout.write(self.style.SUCCESS("Permissions assigned successfully"))
