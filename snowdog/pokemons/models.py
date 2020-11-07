from django.db import models
from django.utils.translation import gettext_lazy as _


class Pokemon(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255, unique=True)
