from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from api.views import InvoiceListView, InvoiceCreateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('api.urls')),
    path('api/invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('api/invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),

    # Frontend pages
    path('', TemplateView.as_view(template_name="index.html"), name="home"),
    path('jobs/', TemplateView.as_view(template_name="jobs.html"), name="jobs-page"),
    path('engineers/', TemplateView.as_view(template_name="engineers.html"), name="engineers-page"),
    path('clients/', TemplateView.as_view(template_name="clients.html"), name="clients-page"),
    path('invoices/', TemplateView.as_view(template_name="invoices.html"), name="invoices-page"),
    path('reports/', TemplateView.as_view(template_name="reports.html"), name="reports-page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
