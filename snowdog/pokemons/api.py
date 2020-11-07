from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from snowdog.pokemons.serializers import PokemonSerializer


class CatchPokemonApiView(CreateAPIView):
    serializer_class = PokemonSerializer
    permission_classes = [AllowAny]


catch_pokemon_api_view = CatchPokemonApiView.as_view()
