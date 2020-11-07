from django.conf.urls import url

from snowdog.pokemons.api import catch_pokemon_api_view

urlpatterns = [
    url('^catch/$', catch_pokemon_api_view, name='catch'),
]
