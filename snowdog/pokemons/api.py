from typing import Union

from django.core.cache import cache
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from snowdog.pokemons.helpers import PokemonApiDataFetcher, day
from snowdog.pokemons.models import Pokemon
from snowdog.pokemons.serializers import PokemonSerializer, PokemonNameSerializer


class PokemonApiViewMixin:
    serializer_class = PokemonSerializer
    permission_classes = [AllowAny]
    queryset = Pokemon.objects.all()


class CatchPokemonApiView(PokemonApiViewMixin,  CreateAPIView):
    def post(self, request: Union[Request, HttpRequest], *args, **kwargs) -> Response:
        serializer = PokemonNameSerializer(data=self.request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name'].lower()
            if response := cache.get(f'{name}'):
                return Response(*response)
            result, status_code = PokemonApiDataFetcher(name).run()
            cache.set(f'{name}', (result, status_code), 1 * day)
            return Response(result, status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


catch_pokemon_api_view = CatchPokemonApiView.as_view()


@method_decorator(cache_page(1 * day), name='dispatch')
class DetailPokemonApiView(PokemonApiViewMixin, RetrieveAPIView):
    pass


detail_pokemon_api_view = DetailPokemonApiView.as_view()
