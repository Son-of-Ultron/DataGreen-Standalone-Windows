from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    class Role(models.TextChoices):
        DONO = "dono", "Dono"
        CONTADOR = "contador", "Contador"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DONO)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.get_role_display()})"


class Client(models.Model):
    class ClientType(models.TextChoices):
        RESIDENCIAL = "Residencial", "Residencial"
        CONDOMINIO = "Condomínio", "Condomínio"
        EMPRESA = "Empresa", "Empresa"

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=32, choices=ClientType.choices)
    phone = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Contract(models.Model):
    class Kind(models.TextChoices):
        MANUTENCAO = "Manutenção mensal", "Manutenção mensal"
        AVULSO = "Serviço avulso", "Serviço avulso"
        PAISAGISMO = "Paisagismo", "Paisagismo"
        PODA = "Poda e limpeza", "Poda e limpeza"

    class Status(models.TextChoices):
        ATIVO = "Ativo", "Ativo"
        ORCAMENTO = "Em orçamento", "Em orçamento"
        CONCLUIDO = "Concluído", "Concluído"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="contracts")
    title = models.CharField(max_length=255)
    kind = models.CharField(max_length=64, choices=Kind.choices)
    monthly_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    status = models.CharField(max_length=32, choices=Status.choices)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.title


class CashEntry(models.Model):
    class Kind(models.TextChoices):
        ENTRADA = "Entrada", "Entrada"
        SAIDA = "Saída", "Saída"

    class Status(models.TextChoices):
        PAGO = "Pago", "Pago"
        PENDENTE = "Pendente", "Pendente"
        CANCELADO = "Cancelado", "Cancelado"

    kind = models.CharField(max_length=16, choices=Kind.choices)
    description = models.CharField(max_length=512)
    category = models.CharField(max_length=128, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=16, choices=Status.choices)
    contract = models.ForeignKey(
        Contract,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cash_entries",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-due_date", "-id"]
        verbose_name_plural = "Cash entries"

    def __str__(self) -> str:
        return self.description


class Invoice(models.Model):
    class Status(models.TextChoices):
        EMITIDA = "Emitida", "Emitida"
        PENDENTE = "Pendente", "Pendente"
        CANCELADA = "Cancelada", "Cancelada"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="invoices")
    number = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=16, choices=Status.choices)
    competence = models.DateField(help_text="Primeiro dia do mês de competência")
    issued_at = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-competence", "-id"]

    def __str__(self) -> str:
        return self.number
