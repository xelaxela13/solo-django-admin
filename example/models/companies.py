from tortoise import fields, Model


class Company(Model):
    id = fields.UUIDField(primary_key=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)
    name = fields.CharField(max_length=255)

    class Meta:
        table = 'companies'

    def __str__(self):
        return self.name
