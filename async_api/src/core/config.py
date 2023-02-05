import os
from logging import config as logging_config

from core.logger import LOGGING

# Apply logging settings
logging_config.dictConfig(LOGGING)

# Project name. Using in Swagger documentation
PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

# Redis Settings
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Elasticsearch Settings
ELASTIC_HOST = os.getenv("ES_HOST", "http://localhost:9200/")

# ROOT
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Auth service
AUTH_HOST = os.getenv("AUTH_HOST", "http://localhost:8001/")
JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY", "JWT_PUBLIC_KEY")
# JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY", "")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
