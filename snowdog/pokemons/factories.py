import factory

from snowdog.pokemons.models import Pokemon


class PokemonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Pokemon

    name = factory.Sequence(lambda n: f'Pokemon {n}')
