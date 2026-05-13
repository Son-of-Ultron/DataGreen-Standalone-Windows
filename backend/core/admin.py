from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from core.models import CashEntry, Client, Contract, Invoice, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fk_name = "user"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "city", "phone", "active")
    list_filter = ("type", "active")
    search_fields = ("name", "city", "phone")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "kind", "status", "monthly_value")
    list_filter = ("kind", "status")
    search_fields = ("title", "client__name")


@admin.register(CashEntry)
class CashEntryAdmin(admin.ModelAdmin):
    list_display = ("description", "kind", "amount", "due_date", "status", "contract")
    list_filter = ("kind", "status")
    search_fields = ("description", "category")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "client", "amount", "status", "competence")
    list_filter = ("status",)
    search_fields = ("number", "client__name")
