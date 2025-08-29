from rest_framework import generics, views
from rest_framework.response import Response
from core.models import Job, Engineer, Client
from .serializers import JobSerializer, EngineerSerializer, ClientSerializer
from rest_framework import viewsets
from core.models import Job, Engineer, TimeEntry, Invoice
from .serializers import JobSerializer, EngineerSerializer, InvoiceSerializer

class JobListView(generics.ListAPIView):
    queryset = Job.objects.select_related("client", "engineer").order_by("-created_at")
    serializer_class = JobSerializer
class EngineerListView(generics.ListAPIView):
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer
class DashboardStatsView(views.APIView):
    def get(self, request, format=None):
        total_jobs = Job.objects.count()
        active_engineers = Engineer.objects.filter(status="online").count()
        completion_rate = 0
        completed = Job.objects.filter(status="completed").count()
        if total_jobs:
            completion_rate = round((completed/total_jobs)*100, 2)
        avg_response_time = "2.4h"
        recent_jobs = Job.objects.select_related("client", "engineer").order_by("-created_at")[:6]
        recent = JobSerializer(recent_jobs, many=True).data
        return Response({
            "total_jobs": total_jobs,
            "active_engineers": active_engineers,
            "completion_rate": completion_rate,
            "avg_response_time": avg_response_time,
            "recent_jobs": recent,
        })

from core.models import Invoice
from .serializers import InvoiceSerializer

class InvoiceListView(generics.ListAPIView):
    queryset = Invoice.objects.all().order_by("-created_at")
    serializer_class = InvoiceSerializer



class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().select_related("client", "engineer")
    serializer_class = JobSerializer

class EngineerViewSet(viewsets.ModelViewSet):
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class EngineerViewSet(viewsets.ModelViewSet):
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().select_related("client", "engineer")
    serializer_class = JobSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().select_related("client")
    serializer_class = InvoiceSerializer
