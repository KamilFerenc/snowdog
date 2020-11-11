# Snowdog Pokemon app

## Setup
*Requirements*
 - It is required to have Docker installed

1) Clone repository `git clone https://github.com/KamilFerenc/snowdog.git`
2) Go to project directory where `Dockerfile` exists
3) Run command `docker build .`
4) Run command `docker-compose up`
5) Open browser eg. `localhost:8000/api/pokemon/`

## Endpoints
1) `GET api/pokemon` - list all pokemons saved in database
2) `GET api/pokemon/?type=electric` - filter all pokemons by type
3) `GET api/pokemon/<id>` - pokemon details
4) `POST api/catch/` - try to get pokemon data from external API

## Tests
1) Login into container `docker-compose run backend bash`
2) Run command `python manage.py test`

## Heroku app
App is deployed at Heroku platform. Has implemented cache mechanism `MemCachier` in order to cache requests.
Visit link and feel free to test it https://snowdog-pokemonapp.herokuapp.com/api/pokemon/

## Testing Heroku
In order to test endpoint `POST` https://snowdog-pokemonapp.herokuapp.com/api/catch use eg. Postman tool (https://www.postman.com/). 
Send in request body data: 
```json
{
	"name": "Pikachu"
}
```
