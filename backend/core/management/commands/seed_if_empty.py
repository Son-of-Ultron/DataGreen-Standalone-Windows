from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import UserProfile


class Command(BaseCommand):
    help = "Cria apenas os usuários iniciais se ainda não existir superusuário. Não cria dados de demonstração."

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Usuários já existem — seed_if_empty ignorado.")
            return

        dono, _ = User.objects.get_or_create(
            username="dono",
            defaults={
                "email": "dono@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        dono.email = "dono@example.com"
        dono.is_staff = True
        dono.is_superuser = True
        dono.set_password("dono123")
        dono.save()
        profile, _ = UserProfile.objects.get_or_create(user=dono, defaults={"role": UserProfile.Role.DONO})
        profile.role = UserProfile.Role.DONO
        profile.save()

        contador, _ = User.objects.get_or_create(
            username="contador",
            defaults={"email": "contador@example.com"},
        )
        contador.email = "contador@example.com"
        contador.set_password("contador123")
        contador.save()
        cprof, _ = UserProfile.objects.get_or_create(user=contador, defaults={"role": UserProfile.Role.CONTADOR})
        cprof.role = UserProfile.Role.CONTADOR
        cprof.save()

        self.stdout.write(self.style.SUCCESS("Usuários iniciais criados: dono/dono123 e contador/contador123"))
