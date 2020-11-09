from functools import cached_property
from typing import Union

import requests
from requests import Response
from rest_framework import status

from snowdog.pokemons.serializers import PokemonSerializer


second = 1
minute = 60 * second
hour = 60 * minute
day = 24 * hour


class PokemonApiDataFetcher:
    ERROR = 'error'

    def __init__(self, name: str):
        self.name = name
        self.url = f"https://pokeapi.co/api/v2/pokemon/{self.name}"

    @cached_property
    def response(self) -> Response:
        return requests.get(self.url)

    def prepare_data(self) -> dict:
        data = self.response.json()
        prepared_data = {}
        prepared_data.update({'name': data.get('name', '')})
        prepared_data.update({'forms': data.get('forms', [])})
        prepared_data.update({'types': data.get('types', [])})
        return prepared_data

    def check_if_valid_data(self) -> bool:
        return self.response.status_code == status.HTTP_200_OK

    def save_pokemon(self) -> Union[str, dict]:
        serializer = PokemonSerializer(data=self.prepare_data())
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.data

    def run(self) -> tuple:
        if self.check_if_valid_data():
            pokemon = self.save_pokemon()
            return pokemon, status.HTTP_201_CREATED
        return self.response.content, status.HTTP_400_BAD_REQUEST
