from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import CashEntry, Client, Contract, Invoice, UserProfile


class Command(BaseCommand):
    help = "Cria usuários demo (dono + contador) e dados de exemplo no PostgreSQL."

    def handle(self, *args, **options):
        dono, _ = User.objects.get_or_create(
            username="dono",
            defaults={
                "email": "dono@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        dono.set_password("dono123")
        dono.save()
        profile, _ = UserProfile.objects.get_or_create(user=dono, defaults={"role": UserProfile.Role.DONO})
        profile.role = UserProfile.Role.DONO
        profile.save()

        contador, _ = User.objects.get_or_create(
            username="contador",
            defaults={"email": "contador@example.com"},
        )
        contador.set_password("contador123")
        contador.save()
        cprof, _ = UserProfile.objects.get_or_create(user=contador, defaults={"role": UserProfile.Role.CONTADOR})
        cprof.role = UserProfile.Role.CONTADOR
        cprof.save()

        if Client.objects.exists():
            self.stdout.write(self.style.WARNING("Já existem clientes; pulando seed de dados de negócio."))
            self.stdout.write(self.style.SUCCESS("Usuários: dono/dono123, contador/contador123"))
            return

        c1 = Client.objects.create(
            name="Condomínio Jardim das Árvores",
            type=Client.ClientType.CONDOMINIO,
            phone="(11) 98888-1200",
            city="São Paulo",
            notes="Manutenção semanal com poda leve e irrigação.",
        )
        c2 = Client.objects.create(
            name="Casa Vila Serena",
            type=Client.ClientType.RESIDENCIAL,
            phone="(11) 97777-4433",
            city="Cotia",
            notes="Cliente recorrente para paisagismo e reposição de mudas.",
        )
        c3 = Client.objects.create(
            name="Clínica Verde Saúde",
            type=Client.ClientType.EMPRESA,
            phone="(11) 96666-9090",
            city="Osasco",
            notes="Jardim de fachada e vasos internos.",
        )

        ct1 = Contract.objects.create(
            client=c1,
            title="Manutenção mensal das áreas comuns",
            kind=Contract.Kind.MANUTENCAO,
            monthly_value=Decimal("8500"),
            status=Contract.Status.ATIVO,
        )
        ct2 = Contract.objects.create(
            client=c2,
            title="Projeto de canteiro ornamental",
            kind=Contract.Kind.PAISAGISMO,
            monthly_value=Decimal("18500"),
            status=Contract.Status.ORCAMENTO,
        )
        ct3 = Contract.objects.create(
            client=c3,
            title="Poda, limpeza e reposição de vasos",
            kind=Contract.Kind.PODA,
            monthly_value=Decimal("4200"),
            status=Contract.Status.ATIVO,
        )

        CashEntry.objects.create(
            kind=CashEntry.Kind.ENTRADA,
            description="Parcela manutenção condomínio",
            category="Recebimento",
            amount=Decimal("8500"),
            due_date=date(2026, 5, 12),
            status=CashEntry.Status.PAGO,
            contract=ct1,
        )
        CashEntry.objects.create(
            kind=CashEntry.Kind.SAIDA,
            description="Mudas ornamentais",
            category="Materiais",
            amount=Decimal("1320"),
            due_date=date(2026, 5, 14),
            status=CashEntry.Status.PAGO,
            contract=ct2,
        )
        CashEntry.objects.create(
            kind=CashEntry.Kind.SAIDA,
            description="Combustível e deslocamento",
            category="Transporte",
            amount=Decimal("480"),
            due_date=date(2026, 5, 16),
            status=CashEntry.Status.PENDENTE,
            contract=ct1,
        )
        CashEntry.objects.create(
            kind=CashEntry.Kind.ENTRADA,
            description="Serviço de poda clínica",
            category="Recebimento",
            amount=Decimal("4200"),
            due_date=date(2026, 5, 20),
            status=CashEntry.Status.PENDENTE,
            contract=ct3,
        )

        Invoice.objects.create(
            client=c1,
            number="NF-2026-0018",
            amount=Decimal("8500"),
            status=Invoice.Status.EMITIDA,
            competence=date(2026, 5, 1),
        )
        Invoice.objects.create(
            client=c3,
            number="NF-2026-0019",
            amount=Decimal("4200"),
            status=Invoice.Status.PENDENTE,
            competence=date(2026, 5, 1),
        )

        self.stdout.write(self.style.SUCCESS("Seed concluído. Login: dono/dono123 ou contador/contador123"))
