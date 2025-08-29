from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, EngineerViewSet, InvoiceViewSet, DashboardStatsView,ClientViewSet

router = DefaultRouter()
router.register("jobs", JobViewSet)
router.register("engineers", EngineerViewSet)
router.register("invoices", InvoiceViewSet)
router.register("clients", ClientViewSet)   # ✅ added


urlpatterns = [
    path("stats/", DashboardStatsView.as_view(), name="api-stats"),
]

urlpatterns += router.urls


