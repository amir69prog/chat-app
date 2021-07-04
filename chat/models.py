from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

User = get_user_model()



## Functions Start
def get_picture(instance,filename):
    path = f'profile_pictures/{instance.user.username}/{instance.user.username}.png'
    return path

def get_default_picture():
    path = 'images/profile.png'
    return path


## Functions End


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=get_picture,default=get_default_picture)
    biography = models.TextField(blank=True,null=True)
    nickname = models.CharField(max_length=255,blank=True,null=True,default='')
    date_craeted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class FriendList(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    friends = models.ManyToManyField(User,blank=True,related_name='friends_user')

    def is_friend(self,user):
        if user in self.friends.all():
            return True
        return False

    def delete_private_chat(self,friend):
        try:
            private_chat_one = ChatRoomPrivate.objects.get(first_user=self.user,secound_user=friend)
            private_chat_one.delete()
        except ChatRoomPrivate.DoesNotExist:
            pass

        try:
            private_chat_two = ChatRoomPrivate.objects.get(first_user=friend,secound_user=self.user)
            private_chat_two.delete()
        except ChatRoomPrivate.DoesNotExist:
            pass

    def remove_friend(self,friend):
        if self.is_friend(friend):
            self.friends.remove(friend)
        his_friends = FriendList.objects.get(user=friend)
        if his_friends.is_friend(self.user):
            his_friends.friends.remove(self.user)
        self.delete_private_chat(friend)

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('requested','Requested'),
        ('accepted','Accepted'),
        ('declined','Declined'),
        ('canceled','Canceled'),
    )

    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver_user')
    status = models.CharField(choices=STATUS_CHOICES,max_length=10,default='requested')
    date_request = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} | {self.receiver.username} | {self.status}'

    def have_request(self):
        sender_to_receiver = FriendRequest.objects.filter(sender=self.sender,receiver=self.receiver,status='requested').exists()
        recever_to_sender = FriendRequest.objects.filter(sender=self.receiver,receiver=self.sender,status='requested').exists()
        if sender_to_receiver or recever_to_sender:
            return True
        return False

    def is_users_in_each_friend_list(self):
        friend_list_receiver = FriendList.objects.get(user=self.receiver)
        friend_list_sender = FriendList.objects.get(user=self.sender)
        if self.sender in friend_list_receiver.friends.all() and self.receiver in friend_list_sender.friends.all():
            return True
        return False

    def create_private_chat(self):
        is_in_each_other = self.is_users_in_each_friend_list()
        if is_in_each_other:
            ChatRoomPrivate.objects.get_or_create(first_user=self.receiver,secound_user=self.sender)

    def insert_users(self):
        # insert sender to receiver friends
        friend_list_receiver = FriendList.objects.get(user=self.receiver)
        if self.receiver not in friend_list_receiver.friends.all():
            friend_list_receiver.friends.add(self.sender)
        
        # insert receiver to sender friends
        friend_list_sender = FriendList.objects.get(user=self.sender)
        if self.sender not in friend_list_sender.friends.all():
            friend_list_sender.friends.add(self.receiver)

    def accept(self):
        self.insert_users()
        self.create_private_chat()

    def save(self):
        pk = self.pk
        # creation
        if not pk:
            if not self.have_request() and (not is_friends(self.sender,self.receiver)):
                super().save()
        else:
            status = self.status
            print(status)
            if status == 'accepted' and (not is_friends(self.sender,self.receiver)):
                self.accept()
            super().save()


class ChatRoomPublic(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name


class ChatRoomPrivate(models.Model):
    first_user = models.ForeignKey(User,on_delete=models.CASCADE)
    secound_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='secound_user_room')

    def __str__(self):
        return f'{self.first_user} | {self.secound_user}'


class MessagePublic(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name=_('Author'))
    content = models.TextField()
    room = models.ForeignKey(ChatRoomPublic,on_delete=models.CASCADE,related_name='messages',null=True,blank=True)
    timestmap = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.author.username


class MessagePrivate(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name=_('Author'))
    content = models.TextField()
    room = models.ForeignKey(ChatRoomPrivate,on_delete=models.CASCADE,related_name='messages',null=True,blank=True)
    timestmap = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.author.username



## Signals Start
@receiver(post_save,sender=User)
def user_method_post_save(sender,instance,created,**ksargs):
    if created:
        FriendList.objects.create(user=instance)
        Profile.objects.create(
            user=instance,
        )

## Signals End


## Functions
def is_friends(sender,receiver):
    friends_list_sender =  FriendList.objects.get(user=sender)
    friends_list_receiver = FriendList.objects.get(user=receiver)
    if friends_list_receiver.is_friend(sender) or friends_list_sender.is_friend(receiver):
        return True
    return False