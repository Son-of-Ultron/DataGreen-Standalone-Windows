from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register(r"clients", views.ClientViewSet, basename="client")
router.register(r"contracts", views.ContractViewSet, basename="contract")
router.register(r"cash-entries", views.CashEntryViewSet, basename="cashentry")
router.register(r"invoices", views.InvoiceViewSet, basename="invoice")

urlpatterns = [
    path("auth/csrf/", views.CsrfView.as_view()),
    path("auth/login/", views.LoginView.as_view()),
    path("auth/logout/", views.LogoutView.as_view()),
    path("auth/me/", views.MeView.as_view()),
    path("bootstrap/", views.BootstrapView.as_view()),
    path("export/monthly/", views.MonthlyExportView.as_view()),
    path("export/full/", views.FullExportView.as_view()),
    path("", include(router.urls)),
]
