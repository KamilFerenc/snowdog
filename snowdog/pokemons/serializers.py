from rest_framework import serializers

from snowdog.pokemons.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ('pk', 'name')
