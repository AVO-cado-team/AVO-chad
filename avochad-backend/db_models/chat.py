from tortoise import Model, fields
from .message import Message
from .user import User

class Chat(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=80)
    chat_name = fields.CharField(max_length=80)
    users = fields.ManyToManyField("models.User", related_name="chats", through="chat_user")
    admin: User = fields.ForeignKeyField("models.User", related_name="admin_chats", on_delete=fields.CASCADE)

    messages: fields.ManyToManyRelation['Message'] = fields.ManyToManyField("models.Message", through="chat_message")
    
    date = fields.DatetimeField(auto_now_add=True)
    is_private = fields.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        table = "chats"