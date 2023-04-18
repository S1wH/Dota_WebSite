from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)

    # или потом сделать через группы?
    is_author = models.BooleanField(default=False)
