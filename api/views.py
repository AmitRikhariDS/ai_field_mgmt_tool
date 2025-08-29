from multiprocessing import context
from django.shortcuts import render
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
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from core.models import Job, Engineer, Invoice, Client

# ---------------- Dashboard ----------------
@login_required
def index(request):
    user = request.user

    jobs = []
    engineers = []
    invoices = []

    # PMO/Admin: full access
    if user.groups.filter(name__in=['PMO', 'Admin']).exists():
        jobs = Job.objects.all()
        engineers = Engineer.objects.all()
        invoices = Invoice.objects.all()

    # Field Engineer: only their assigned jobs
    elif user.groups.filter(name='Field Engineer').exists():
        try:
            engineer = Engineer.objects.get(user=user)
            jobs = Job.objects.filter(engineer=engineer)
            invoices = Invoice.objects.filter(job__engineer=engineer)
        except Engineer.DoesNotExist:
            jobs = Job.objects.none()
            invoices = Invoice.objects.none()

    # Account Team: invoices and reports only
    elif user.groups.filter(name='Account Team').exists():
        invoices = Invoice.objects.all()
        jobs = Job.objects.none()
        engineers = Engineer.objects.none()

    # Client: only their own jobs/invoices
    elif user.groups.filter(name='Client').exists():
        try:
            client = Client.objects.get(user=user)
            jobs = Job.objects.filter(client=client)
            invoices = Invoice.objects.filter(client=client)
        except Client.DoesNotExist:
            jobs = Job.objects.none()
            invoices = Invoice.objects.none()

    return render(request, 'index.html', {
        'jobs': jobs,
        'engineers': engineers,
        'invoices': invoices
    })

# ---------------- Optional: API Views ----------------
from rest_framework import viewsets
from .serializers import JobSerializer, EngineerSerializer, InvoiceSerializer
from core.models import Job, Engineer, Invoice
from rest_framework.permissions import IsAuthenticated

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

class EngineerViewSet(viewsets.ModelViewSet):
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer
    permission_classes = [IsAuthenticated]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def jobs_page(request):
    return render(request, 'jobs.html')

@login_required
def engineers_page(request):
    return render(request, 'engineers.html')

@login_required
def clients_page(request):
    return render(request, 'clients.html')

@login_required
def invoices_page(request):
    return render(request, 'invoices.html')

@login_required
def reports_page(request):
    return render(request, 'reports.html')


# api/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')  # new logout page

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    total_jobs = Job.objects.count()
    active_engineers = Engineer.objects.filter(status='active').count()
    completion_rate = 75  # replace with actual calculation
    avg_response_time = 2  # replace with actual calculation
    recent_jobs = Job.objects.order_by('-id')[:5]

    context = {
        'total_jobs': total_jobs,
        'active_engineers': active_engineers,
        'completion_rate': completion_rate,
        'avg_response_time': avg_response_time,
        'recent_jobs': recent_jobs,
    }
    return render(request, 'index.html', context)
# api/views.py
from rest_framework import generics
from core.models import Client
from .serializers import ClientSerializer
from rest_framework.permissions import IsAuthenticated

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
