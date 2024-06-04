from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """ this model created to make the user model as editable"""
    email = models.EmailField(unique=True, verbose_name=_('email'))
