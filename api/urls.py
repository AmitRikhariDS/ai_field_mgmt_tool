from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, EngineerViewSet, InvoiceViewSet, DashboardStatsView,ClientViewSet,TimeEntryViewSet,InvoiceDetailView,InvoiceCreateView, InvoiceListView,ClientListCreateView
# from api.views import InvoiceListCreateAPIView, InvoiceRetrieveAPIView



router = DefaultRouter()
router.register("jobs", JobViewSet)
router.register("engineers", EngineerViewSet)
router.register("invoices", InvoiceViewSet)
router.register("clients", ClientViewSet)   # ✅ added
router.register(r'timeentries', TimeEntryViewSet)



urlpatterns = [
    path("stats/", DashboardStatsView.as_view(), name="api-stats"),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('clients/', ClientListCreateView.as_view(), name='client-list-create')
]


urlpatterns += router.urls


