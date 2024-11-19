from django.contrib import admin

from django_app.models import AccountsPermission, Account, Permission, Company


class PermissionsInline(admin.StackedInline):
    model = AccountsPermission
    extra = 3


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    ...


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    ...
