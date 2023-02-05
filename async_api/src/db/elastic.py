from typing import Optional

from elasticsearch import AsyncElasticsearch

es: Optional[AsyncElasticsearch] = None


# Function will be useful when implementing dependencies
async def get_elastic() -> AsyncElasticsearch:
    return es
