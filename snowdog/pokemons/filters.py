from django_filters import rest_framework as filters

from snowdog.pokemons.models import Pokemon


class PokemonFilter(filters.FilterSet):
    type = filters.CharFilter(field_name='types__name', lookup_expr='iexact')

    class Meta:
        model = Pokemon
        fields = ('type',)
