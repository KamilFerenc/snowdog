import responses
from django.test import TestCase
from django.urls import reverse

from snowdog.pokemons.models import Pokemon


class CatchPokemonApiViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('catch')
        self.data = {'name': 'pikachu'}

    @responses.activate
    def test_valid_name(self):
        api_data = {
            "name": "pikachu",
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
        responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/pikachu',
                      json=api_data, status=200)
        self.assertEqual(Pokemon.objects.count(), 0)
        resp = self.client.post(self.url, self.data)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, 'https://pokeapi.co/api/v2/pokemon/pikachu')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Pokemon.objects.count(), 1)
        data = resp.json()
        self.assertEqual(data['name'], api_data['name'])
        self.assertEqual(data['forms'], api_data['forms'])
        self.assertEqual(data['types'], api_data['types'])

    def test_empty_name(self):
        self.data['name'] = ''
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['name'], ['This field may not be blank.'])
