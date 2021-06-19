from chat.views import room
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name



class Message(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name=_('Author'))
    content = models.TextField()
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='messages',null=True,blank=True)
    timestmap = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.author.username
