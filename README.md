# Movie Theater API
The following services are used: FastAPI, Django, Nginx, Postgres, ElasticSearch, Kibana, Redis

## API endpoints
- OpenAPI: http://localhost:8000/api/openapi
- Movies list: http://localhost:8000/api/v1/film/
- Movie by UUID: http://localhost:8000/api/v1/film/2a090dde-f688-46fe-a9f4-b781a985275e
- Similar moview: http://localhost:8000/api/v1/film/2a090dde-f688-46fe-a9f4-b781a985275e/alike
- Fuzzy movie search: http://localhost:8000/api/v1/film/search/dog
- Sorting movies by rating: http://localhost:8000/api/v1/film/?sort=-imdb_rating
- Sorting movies with pagination: http://localhost:8000/api/v1/film/?sort=-imdb_rating&page_size=10&page_number=3
- Sorting movies with pagination and filtering by genre: http://localhost:8000/api/v1/film/?sort=-imdb_rating&page_size=10&page_number=5&filter_genre=120a21cf-9097-479e-904a-13dd7198c1dd
- Popular movies in the genre: http://localhost:8000/api/v1/film/genre/120a21cf-9097-479e-904a-13dd7198c1dd
- Persons list: http://localhost:8000/api/v1/person/
- Person's info by UUID: http://localhost:8000/api/v1/person/05d92f4a-b55c-45f6-9200-41f153a72a7a
- Person search http://localhost:8000/api/v1/person/search/adam
- Genres list: http://localhost:8000/api/v1/genre/
- Genre by UUID:: http://localhost:8000/api/v1/genre/c020dab2-e9bd-4758-95ca-dbe363462173

## How to deploy
> 1. `cd tests/functional/`
> 2. `make build`
> 3. `make start`
> 4. For stopping: `make stop`