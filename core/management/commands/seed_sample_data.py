from django.core.management.base import BaseCommand
from core.models import Client, Engineer, Job
import random
from django.utils import timezone
class Command(BaseCommand):
    help = "Seed sample clients, engineers and jobs"
    def handle(self, *args, **options):
        clients = ["Global Tech Inc.", "Data Solutions Ltd", "Cloud Innovators", "Networking Pros"]
        eng_names = ["John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis"]
        created_clients = []
        for c in clients:
            created_clients.append(Client.objects.create(name=c))
        created_eng = []
        for n in eng_names:
            created_eng.append(Engineer.objects.create(name=n, status=random.choice(["online","busy","offline"])))
        for i in range(1, 9):
            Job.objects.create(
                job_code=f"JOB-{1000+i}",
                title=f"Site visit #{i}",
                client=random.choice(created_clients),
                engineer=random.choice(created_eng),
                status=random.choice(["pending","in_progress","completed","scheduled"]),
                priority=random.choice(["low","medium","high"]),
                scheduled_date=timezone.now().date()
            )
        self.stdout.write(self.style.SUCCESS("Seeded sample data"))
