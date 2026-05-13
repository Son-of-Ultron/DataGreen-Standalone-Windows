from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import CashEntry, Client, Contract, Invoice, UserProfile

_MONTHS_PT = (
    "",
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
)


def competence_label(d: date) -> str:
    return f"{_MONTHS_PT[d.month]}/{d.year}"


_MONTH_NAME_TO_INT = {name: idx for idx, name in enumerate(_MONTHS_PT) if name}


def parse_competence_month(value: str | None) -> date | None:
    if not value or not isinstance(value, str):
        return None
    value = value.strip()
    if not value:
        return None
    if value.count("-") == 2 and len(value) >= 10:
        y, m, _ = value[:10].split("-")
        return date(int(y), int(m), 1)
    parts = value.split("/")
    if len(parts) != 2:
        return None
    month_name, year_s = parts[0].strip(), parts[1].strip()
    m = _MONTH_NAME_TO_INT.get(month_name)
    if not m:
        return None
    return date(int(year_s), m, 1)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "role")

    def get_role(self, obj: User) -> str:
        profile = getattr(obj, "profile", None)
        if profile:
            return profile.role
        return UserProfile.Role.DONO


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id", "name", "type", "phone", "city", "notes", "active", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")


class ContractSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = Contract
        fields = (
            "id",
            "client",
            "title",
            "kind",
            "monthly_value",
            "status",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def to_representation(self, instance: Contract) -> dict:
        return {
            "id": instance.id,
            "clientId": instance.client_id,
            "title": instance.title,
            "kind": instance.kind,
            "monthlyValue": float(instance.monthly_value),
            "status": instance.status,
            "startDate": instance.start_date.isoformat() if instance.start_date else None,
            "endDate": instance.end_date.isoformat() if instance.end_date else None,
            "createdAt": instance.created_at.isoformat(),
            "updatedAt": instance.updated_at.isoformat(),
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            return super().to_internal_value(data)
        mv = data.get("monthlyValue", data.get("monthly_value", 0))
        if isinstance(mv, str):
            mv = mv.replace(".", "").replace(",", ".")
        payload = {
            "client": data.get("clientId", data.get("client_id")),
            "title": data.get("title", ""),
            "kind": data.get("kind", ""),
            "monthly_value": mv,
            "status": data.get("status", ""),
            "start_date": data.get("startDate", data.get("start_date")) or None,
            "end_date": data.get("endDate", data.get("end_date")) or None,
        }
        return super().to_internal_value(payload)


class CashEntrySerializer(serializers.ModelSerializer):
    contract = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = CashEntry
        fields = (
            "id",
            "kind",
            "description",
            "category",
            "amount",
            "due_date",
            "status",
            "contract",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def to_representation(self, instance: CashEntry) -> dict:
        return {
            "id": instance.id,
            "kind": instance.kind,
            "description": instance.description,
            "category": instance.category,
            "amount": float(instance.amount),
            "dueDate": instance.due_date.isoformat(),
            "status": instance.status,
            "contract_id": instance.contract_id,
            "createdAt": instance.created_at.isoformat(),
            "updatedAt": instance.updated_at.isoformat(),
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            return super().to_internal_value(data)
        due = data.get("dueDate", data.get("due_date"))
        cid = data.get("contractId", data.get("contract_id"))
        amt = data.get("amount", 0)
        if isinstance(amt, str):
            amt = amt.replace(".", "").replace(",", ".")
        payload = {
            "kind": data.get("kind", ""),
            "description": data.get("description", ""),
            "category": data.get("category", ""),
            "amount": amt,
            "due_date": due,
            "status": data.get("status", ""),
            "contract": cid if cid not in ("", None) else None,
        }
        return super().to_internal_value(payload)


class InvoiceSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = Invoice
        fields = (
            "id",
            "client",
            "number",
            "amount",
            "status",
            "competence",
            "issued_at",
            "due_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def to_representation(self, instance: Invoice) -> dict:
        return {
            "id": instance.id,
            "clientId": instance.client_id,
            "number": instance.number,
            "amount": float(instance.amount),
            "status": instance.status,
            "month": competence_label(instance.competence),
            "competence": instance.competence.isoformat(),
            "issuedAt": instance.issued_at.isoformat() if instance.issued_at else None,
            "dueDate": instance.due_date.isoformat() if instance.due_date else None,
            "createdAt": instance.created_at.isoformat(),
            "updatedAt": instance.updated_at.isoformat(),
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            return super().to_internal_value(data)
        comp = data.get("competence") or data.get("competence_date")
        if not comp:
            comp = parse_competence_month(data.get("month"))
        amt = data.get("amount", 0)
        if isinstance(amt, str):
            amt = amt.replace(".", "").replace(",", ".")
        payload = {
            "client": data.get("clientId", data.get("client_id")),
            "number": data.get("number", ""),
            "amount": amt,
            "status": data.get("status", ""),
            "competence": comp,
            "issued_at": data.get("issuedAt", data.get("issued_at")) or None,
            "due_date": data.get("dueDate", data.get("due_date")) or None,
        }
        return super().to_internal_value(payload)

    def validate_amount(self, value):
        if isinstance(value, str):
            cleaned = value.replace(".", "").replace(",", ".")
            value = Decimal(cleaned)
        return value

    def validate_competence(self, value):
        if value is None:
            raise serializers.ValidationError("Competência inválida (use mês/ano ou data YYYY-MM-DD).")
        if value.day != 1:
            return date(value.year, value.month, 1)
        return value
