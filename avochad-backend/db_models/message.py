from tortoise import Model, fields


class Message(Model):
    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=500)
    chat = fields.ForeignKeyField("models.Chat")
    user = fields.ForeignKeyField("models.User")
    reply_to = fields.ForeignKeyField("models.Message", related_name="message_reply_to", null=True)
    date = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        table = "messages"