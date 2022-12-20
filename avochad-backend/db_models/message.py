from tortoise import Model, fields


class Message(Model):
    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=500)
    chat = fields.ForeignKeyField("models.Chat", related_name="message_chat")
    user = fields.ForeignKeyField("models.User", related_name="message_user")
    date = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        table = "messages"