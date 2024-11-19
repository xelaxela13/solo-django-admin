from django.db import models

from models.accounts import Account as FastAPIAccount, \
    Permission as FastAPIPermission
from models.companies import Company as FastAPICompany
from solo_django_admin.models import MapperModel


class AccountsPermission(models.Model):
    accounts = models.ForeignKey("django_app.Account",
                                 primary_key=True,
                                 on_delete=models.CASCADE)
    permission = models.ForeignKey("django_app.Permission",
                                   on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts_permission'
        unique_together = (('accounts', 'permission'),)
        managed = False
        auto_created = True


class Account(MapperModel):
    fast_api_model = FastAPIAccount
    permissions_related_path = "django_app.Permission"
    company_related_path = "django_app.Company"

    permissions = models.ManyToManyField(
        'django_app.Permission',
        related_name='accounts',
        through=AccountsPermission,
        blank=True,
    )


class Company(MapperModel):
    fast_api_model = FastAPICompany


class Permission(MapperModel):
    fast_api_model = FastAPIPermission
