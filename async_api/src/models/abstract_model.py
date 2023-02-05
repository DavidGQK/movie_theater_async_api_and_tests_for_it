import orjson
# pydantic transferring data from json to objects
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, а pydantic needs unicode, thas's why we decode
    return orjson.dumps(v, default=default).decode()


class AbstractModel(BaseModel):
    class Config:
        # Change standard processing json to faster
        json_loads = orjson.loads
        json_dumps = orjson_dumps
