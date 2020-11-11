import factory

from snowdog.pokemons.models import Pokemon, PokemonType


class PokemonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Pokemon

    name = factory.Sequence(lambda n: f'Pokemon {n}')


class PokemonTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = PokemonType

    pokemon = factory.SubFactory(PokemonFactory)
    name = factory.Sequence(lambda n: f'Type_{n}')
    slot = factory.Sequence(lambda n: n)
    type = {}

