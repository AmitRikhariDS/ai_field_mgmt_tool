from rest_framework import generics, views
from rest_framework.response import Response
from core.models import Job, Engineer, Client
from .serializers import JobSerializer, EngineerSerializer, ClientSerializer
from rest_framework import viewsets
from core.models import Job, Engineer, TimeEntry, Invoice
from .serializers import JobSerializer, EngineerSerializer
#,InvoiceSerializer
from rest_framework import viewsets, generics
from core.models import Job, Client, Engineer, Invoice
from .serializers import JobSerializer, ClientSerializer, EngineerSerializer,TimeEntrySerializer

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

# class InvoiceListView(generics.ListAPIView):
#     queryset = Invoice.objects.all().order_by("-created_at")
#     serializer_class = InvoiceSerializer



class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().select_related("client", "engineer")
    serializer_class = JobSerializer

class EngineerViewSet(viewsets.ModelViewSet):
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer

# class InvoiceViewSet(viewsets.ModelViewSet):
#     queryset = Invoice.objects.all()
#     serializer_class = InvoiceSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class EngineerViewSet(viewsets.ModelViewSet):
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer

# api/views.py
from rest_framework import viewsets
from .serializers import JobSerializer
from django_filters.rest_framework import DjangoFilterBackend # pyright: ignore[reportMissingImports]
from rest_framework import filters

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-scheduled_date')
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status', 'client', 'engineer']
    search_fields = ['title', 'job_code']
    ordering_fields = ['scheduled_date', 'priority']


# class InvoiceViewSet(viewsets.ModelViewSet):
#     queryset = Invoice.objects.all().select_related("client")
#     serializer_class = InvoiceSerializer




class EngineerViewSet(viewsets.ModelViewSet):
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer



# ---------- Client ----------
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# ---------- Engineer ----------
class EngineerViewSet(viewsets.ModelViewSet):
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer

# ---------- Job ----------
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer

# ---------- Invoice ----------
# class InvoiceViewSet(viewsets.ModelViewSet):
#     queryset = Invoice.objects.all().order_by('-created_at')
#     serializer_class = InvoiceSerializer

# api/views.py
class TimeEntryViewSet(viewsets.ModelViewSet):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-date')
    serializer_class = InvoiceSerializer


from rest_framework import generics
from core.models import Invoice
from .serializers import InvoiceSerializer

class InvoiceCreateView(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceListView(generics.ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceDetailView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


# from rest_framework import generics
# from rest_framework.permissions import AllowAny
# from core.models import Invoice
# from .serializers import InvoiceSerializer

# class InvoiceListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Invoice.objects.all().order_by('-date')
#     serializer_class = InvoiceSerializer
#     permission_classes = [AllowAny]  # remove or restrict in production

# class InvoiceRetrieveAPIView(generics.RetrieveAPIView):
#     queryset = Invoice.objects.all()
#     serializer_class = InvoiceSerializer
#     permission_classes = [AllowAny]

