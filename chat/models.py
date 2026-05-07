from django.db import models
from account.models import User

# Create your models here.
class Messages(models.Model):
    body=models.TextField()
    sent_by=models.CharField(max_length=255)
    created_at=models.DateField(auto_now_add=True)
    created_by=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL)
    class Meta:
        ordering=('created_at',)
    def __str__(self):
        return f'{self.sent_by}'
    


class Room(models.Model):
    WAITING='waiting'
    ACTIVE='active'
    CLOSED='closed'

    choices_status=(
        (WAITING,'Waiting'),
        (ACTIVE,'Active'),
        (CLOSED,'Closed')
    )
    uuid=models.CharField(max_length=255)
    client=models.CharField(max_length=255)
    agent=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL)
    messages=models.ManyToManyField(Messages,blank=True)
    url=models.CharField(max_length=200,blank=True)
    status=models.CharField(max_length=20,choices=choices_status,default=WAITING)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created_at',)
    def __str__(self):
        return f'{self.client}-{self.uuid}'
