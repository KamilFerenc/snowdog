from django.test import TestCase
from django.utils.translation import gettext_lazy  as _

from snowdog.pokemons.factories import PokemonFactory
from snowdog.pokemons.models import Pokemon
from snowdog.pokemons.serializers import PokemonNameSerializer, PokemonSerializer


class PokemonNameSerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = PokemonNameSerializer
        self.pokemon_name = 'pikachu'
        self.pokemon = PokemonFactory(name=self.pokemon_name)
        self.data = {'name': self.pokemon_name}

    def test_serializer_valid(self):
        self.data['name'] = 'pokemon_name'
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid(self):
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        expected_error = _(f'Pokemon with name {self.pokemon_name} already exists in database.')
        self.assertIn(expected_error, serializer.errors['name'])


class PokemonSerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = PokemonSerializer
        self.data = {
            "name": "butterfree",
            "forms": [
                {
                    "url": "https://pokeapi.co/api/v2/pokemon-form/12/",
                    "name": "butterfree"
                }
            ],
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "url": "https://pokeapi.co/api/v2/type/7/",
                        "name": "bug"
                    }
                },
                {
                    "slot": 2,
                    "type": {
                        "url": "https://pokeapi.co/api/v2/type/3/",
                        "name": "flying"
                    }
                }
            ]
        }

    def test_serializer_valid(self):
        self.assertFalse(Pokemon.objects.exists())
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        pokemon = serializer.save()
        self.assertTrue(Pokemon.objects.exists())
        self.assertEqual(pokemon.name, self.data['name'])
        self.assertEqual(pokemon.types.count(), len(self.data['types']))
