from typing import Union

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from snowdog.pokemons.models import Pokemon, PokemonType


class PokemonNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)

    def validate_name(self,  name: str) -> Union[str, serializers.ValidationError]:
        if Pokemon.objects.filter(name=name).exists():
            raise serializers.ValidationError(_(f'Pokemon with name {name} already exists in database.'))
        elif name.isnumeric():
            raise serializers.ValidationError(_('Pokemon name can not be a numeric value.'))
        return name


class PokemonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonType
        fields = ('slot', 'type')


class PokemonSerializer(serializers.ModelSerializer):
    types = PokemonTypeSerializer(many=True)
    forms = serializers.JSONField()

    class Meta:
        model = Pokemon
        fields = ('id', 'name',  'forms', 'types')

    def create(self, validate_data) -> Pokemon:
        types = self.validated_data.pop('types', [])
        pokemon = Pokemon.objects.create(**self.validated_data)
        for pokemon_type in types:
            PokemonType.objects.create(name=pokemon_type['type']['name'],
                                       slot=pokemon_type['slot'],
                                       type=pokemon_type['type'],
                                       pokemon=pokemon)
        return pokemon

