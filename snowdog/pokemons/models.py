from django.db import models
from django.utils.translation import gettext_lazy as _


class Pokemon(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255, unique=True)
    forms = models.JSONField(verbose_name=_('Forms'), blank=True, null=True)


class PokemonType(models.Model):
    pokemon = models.ForeignKey('Pokemon', verbose_name=_('Pokemon'), on_delete=models.CASCADE, related_name='types')
    name = models.CharField(verbose_name=_('Type name'), max_length=255)
    slot = models.IntegerField(verbose_name=_('Type slot'))
    type = models.JSONField(verbose_name=_('Type'))

