from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=80)
    last_name = fields.CharField(max_length=80)
    username = fields.CharField(max_length=80, unique=True)
    email = fields.CharField(max_length=80, unique=True)
    password = fields.CharField(max_length=80)

    def __str__(self):
        return self.first_name

    class Meta:
        table = "users"