from unittest import mock

import responses
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError

from snowdog.pokemons.helpers import PokemonApiDataFetcher
from snowdog.pokemons.models import Pokemon


class PokemonApiDataFetcherTest(TestCase):
    def setUp(self) -> None:
        self.pokemon_api_fetcher = PokemonApiDataFetcher
        self.pokemon_name = 'pikachu'

    @responses.activate
    def test_prepare_data(self):
        api_data = {
            "name": f"{self.pokemon_name}",
            "forms": [
                {
                    "name": "pikachu",
                    "url": "https://pokeapi.co/api/v2/pokemon-form/25/"
                }
            ],
        }
        responses.add(responses.GET, f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_name}',
                      json=api_data, status=200)
        result = self.pokemon_api_fetcher(self.pokemon_name).prepare_data()
        expected_result = {
            "name": f"{self.pokemon_name}",
            "forms": [
                {
                    "name": "pikachu",
                    "url": "https://pokeapi.co/api/v2/pokemon-form/25/"
                }
            ],
            'types': []
        }
        self.assertDictEqual(expected_result, result)

    @responses.activate
    def test_check_if_valid_data_true(self):
        responses.add(responses.GET, f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_name}',
                      json={}, status=200)
        self.assertTrue(self.pokemon_api_fetcher(self.pokemon_name).check_if_valid_data())
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_check_if_valid_data_false(self):
        responses.add(responses.GET, f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_name}',
                      json={}, status=400)
        self.assertFalse(self.pokemon_api_fetcher(self.pokemon_name).check_if_valid_data())
        self.assertEqual(len(responses.calls), 1)

    @mock.patch('snowdog.pokemons.helpers.PokemonApiDataFetcher.prepare_data')
    def test_save_pokemon(self, mock_prepare_data):
        data = {
            "name": f"{self.pokemon_name}",
            "forms": [
                {
                    "name": "pikachu",
                    "url": "https://pokeapi.co/api/v2/pokemon-form/25/"
                }
            ],
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "url": "https://pokeapi.co/api/v2/type/13/",
                        "name": "electric"
                    }
                }
            ]
        }
        mock_prepare_data.return_value = data
        self.assertFalse(Pokemon.objects.exists())
        result = self.pokemon_api_fetcher(self.pokemon_name).save_pokemon()
        mock_prepare_data.assert_called_once()
        pokemon = Pokemon.objects.get(name=self.pokemon_name)
        self.assertEqual(result['id'], pokemon.pk)
        self.assertEqual(result['name'], self.pokemon_name)
        self.assertEqual(pokemon.types.count(), len(data['types']))
        self.assertEqual(pokemon.types.first().name, data['types'][0]['type']['name'])

    @mock.patch('snowdog.pokemons.helpers.PokemonApiDataFetcher.prepare_data')
    def test_save_pokemon_invalid_data(self, mock_prepare_data):
        data = {
            "name": f"{self.pokemon_name}",
            "types": []
        }
        mock_prepare_data.return_value = data
        self.assertFalse(Pokemon.objects.exists())
        with self.assertRaises(ValidationError):
            self.pokemon_api_fetcher(self.pokemon_name).save_pokemon()
        mock_prepare_data.assert_called_once()
        self.assertFalse(Pokemon.objects.exists())

    @responses.activate
    def test_run_invalid_api_response(self):
        wrong_name = 'wrong_name'
        responses.add(responses.GET, f'https://pokeapi.co/api/v2/pokemon/{wrong_name}',
                      json={'error': 'Not Found'}, status=400)
        result, status_code = self.pokemon_api_fetcher(wrong_name).run()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(result, b'{"error": "Not Found"}')
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)

    @responses.activate
    def test_run_valid_api_response(self):
        data = {
            "name": f"{self.pokemon_name}",
            "forms": [
                {
                    "name": "pikachu",
                    "url": "https://pokeapi.co/api/v2/pokemon-form/25/"
                }
            ],
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "url": "https://pokeapi.co/api/v2/type/13/",
                        "name": "electric"
                    }
                }
            ]
        }
        responses.add(responses.GET, f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_name}',
                      json=data, status=200)
        self.assertFalse(Pokemon.objects.exists())
        result, status_code = self.pokemon_api_fetcher(self.pokemon_name).run()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(result['name'], self.pokemon_name)
        self.assertEqual(status_code, status.HTTP_201_CREATED)
