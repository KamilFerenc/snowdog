from django.conf.urls import url

from snowdog.pokemons.api import catch_pokemon_api_view, detail_pokemon_api_view, list_pokemon_api_view

urlpatterns = [
    url('^catch/$', catch_pokemon_api_view, name='catch'),
    url(r'^pokemon/$', list_pokemon_api_view, name='list'),
    url(r'^pokemon/(?P<pk>\d+)$', detail_pokemon_api_view, name='detail'),
]
