from tortoise import fields, Model


class Account(Model):
    id = fields.UUIDField(primary_key=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)
    username = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    company = fields.ForeignKeyField(
        'models.Company',
        on_delete=fields.CASCADE,
        related_name='accounts'
    )
    permissions = fields.ManyToManyField(
        "models.Permission",
        related_name='accounts',
    )

    class Meta:
        table = 'accounts'

    def __str__(self):
        return self.username


class Permission(Model):
    id = fields.UUIDField(primary_key=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name
