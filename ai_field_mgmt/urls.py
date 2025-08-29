from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', TemplateView.as_view(template_name="index.html"), name="home"),
    path('jobs/', TemplateView.as_view(template_name="jobs.html"), name="jobs-page"),
    path('engineers/', TemplateView.as_view(template_name="engineers.html"), name="engineers-page"),
    path('invoices/', TemplateView.as_view(template_name="invoices.html"), name="invoices-page"),
    path('clients/', TemplateView.as_view(template_name="clients.html"), name="clients-page"),  # ✅ new
]
