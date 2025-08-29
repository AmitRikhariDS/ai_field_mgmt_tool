from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from api import views
from api.views import (
    InvoiceListView,
    InvoiceCreateView,
    index,           # make sure these views exist in api/views.py
    jobs_page,
    engineers_page,
    clients_page,
    invoices_page,
    reports_page
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('api.urls')),
    path('api/invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('api/invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),

    # Frontend pages
    path('', index, name='dashboard'),
    path('jobs/', jobs_page, name="jobs-page"),
    path('engineers/', engineers_page, name="engineers-page"),
    path('clients/', clients_page, name="clients-page"),
    path('invoices/', invoices_page, name="invoices-page"),
    path('reports/', reports_page, name="reports-page"),

    # Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ai_field_mgmt/urls.py


