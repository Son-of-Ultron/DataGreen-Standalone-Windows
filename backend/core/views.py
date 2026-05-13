from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from core.export_service import csv_response, full_xlsx_response, xlsx_response
from core.models import CashEntry, Client, Contract, Invoice
from core.permissions import IsDono
from core.serializers import (
    CashEntrySerializer,
    ClientSerializer,
    ContractSerializer,
    InvoiceSerializer,
    LoginSerializer,
    UserSerializer,
)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"detail": "ok"})


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=ser.validated_data["username"],
            password=ser.validated_data["password"],
        )
        if not user:
            return Response({"detail": "Credenciais inválidas."}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class BootstrapView(APIView):
    def get(self, request):
        # Mantém payload inicial leve para uso local de longo prazo.
        since_date = timezone.localdate() - timedelta(days=730)
        clients = Client.objects.filter(active=True).order_by("name")
        contracts = Contract.objects.select_related("client").order_by("-id")
        cash = (
            CashEntry.objects.select_related("contract")
            .filter(due_date__gte=since_date)
            .order_by("-due_date", "-id")
        )
        invoices = (
            Invoice.objects.select_related("client")
            .filter(competence__gte=since_date)
            .order_by("-competence", "-id")
        )
        return Response(
            {
                "user": UserSerializer(request.user).data,
                "clients": ClientSerializer(clients, many=True).data,
                "contracts": ContractSerializer(contracts, many=True).data,
                "cash": CashEntrySerializer(cash, many=True).data,
                "invoices": InvoiceSerializer(invoices, many=True).data,
            }
        )


class DonoWriteMixin:
    def get_permissions(self):
        perms = [permissions.IsAuthenticated()]
        if self.action not in ("list", "retrieve"):
            perms.append(IsDono())
        return perms


class ClientViewSet(DonoWriteMixin, viewsets.ModelViewSet):
    queryset = Client.objects.filter(active=True).order_by("name")
    serializer_class = ClientSerializer


class ContractViewSet(DonoWriteMixin, viewsets.ModelViewSet):
    queryset = Contract.objects.select_related("client").order_by("-id")
    serializer_class = ContractSerializer


class CashEntryViewSet(DonoWriteMixin, viewsets.ModelViewSet):
    queryset = CashEntry.objects.select_related("contract").order_by("-due_date", "-id")
    serializer_class = CashEntrySerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, IsDono])
    def cancel(self, request, pk=None):
        cash_entry = self.get_object()
        if cash_entry.status == CashEntry.Status.CANCELADO:
            return Response({"detail": "Lançamento já está cancelado."}, status=status.HTTP_400_BAD_REQUEST)
        cash_entry.status = CashEntry.Status.CANCELADO
        cash_entry.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(cash_entry).data, status=status.HTTP_200_OK)


class InvoiceViewSet(DonoWriteMixin, viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related("client").order_by("-competence", "-id")
    serializer_class = InvoiceSerializer


class MonthlyExportView(APIView):
    def get(self, request):
        try:
            year = int(request.query_params.get("year", ""))
            month = int(request.query_params.get("month", ""))
        except ValueError:
            return Response({"detail": "Informe year e month numéricos."}, status=status.HTTP_400_BAD_REQUEST)
        if month < 1 or month > 12:
            return Response({"detail": "month deve ser 1–12."}, status=status.HTTP_400_BAD_REQUEST)
        fmt = (request.query_params.get("format") or "csv").lower()
        if fmt == "xlsx":
            return xlsx_response(year, month)
        if fmt == "csv":
            return csv_response(year, month)
        return Response({"detail": "format deve ser csv ou xlsx."}, status=status.HTTP_400_BAD_REQUEST)


class FullExportView(APIView):
    def get(self, request):
        return full_xlsx_response()
