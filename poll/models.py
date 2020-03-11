from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Poll(models.Model):
    subject = models.CharField(max_length=100)
    detail = models.TextField(default='')
    picture = models.ImageField(upload_to="decoration/image", null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    password = models.CharField(max_length=100, default='')
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class Poll_Choice(models.Model):
    subject = models.CharField(max_length=100)
    image = models.ImageField(upload_to="decoration/image", null=True)
    poll_id = models.ForeignKey("poll.Poll", on_delete=models.CASCADE)

    def __str__(self):
        return self.subject
    

class Poll_Vote(models.Model):
    poll_id = models.ForeignKey("poll.Poll", on_delete=models.CASCADE)
    choice_id = models.ForeignKey("poll.Poll_Choice", on_delete=models.CASCADE)
    vote_by = models.ForeignKey(User, on_delete=models.CASCADE)

    