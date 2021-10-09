from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    image = models.ImageField(upload_to='accounts', default='user.png')
    credit = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
