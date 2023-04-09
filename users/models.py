from django.db import models
from django.contrib.auth.models import User, AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)





