from typing import Union

from django.http import HttpRequest
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from snowdog.pokemons.helpers import PokemonApiDataFetcher
from snowdog.pokemons.serializers import PokemonSerializer, PokemonNameSerializer


class CatchPokemonApiView(CreateAPIView):
    serializer_class = PokemonSerializer
    permission_classes = [AllowAny]

    def post(self, request: Union[Request, HttpRequest], *args, **kwargs) -> Response:
        serializer = PokemonNameSerializer(data=self.request.data)
        if serializer.is_valid():
            result, status_code = PokemonApiDataFetcher(serializer.validated_data['name']).run()
            return Response(result, status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


catch_pokemon_api_view = CatchPokemonApiView.as_view()
