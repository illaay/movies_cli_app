import pymongo
from functools import wraps
from pymongo.errors import ConnectionFailure
from errors import MongoDBConnectionError


def create_mongo_connection(config_dict):
    try:
        client = pymongo.MongoClient(config_dict["uri"])
        client.admin.command("ping")
        return client[config_dict["database"]][config_dict["collection"]]
    except ConnectionFailure:
        raise MongoDBConnectionError("Ошибка подключения к MongoDB-серверу")


def check_mongo_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for _ in range(2):
            try:
                return func(*args, **kwargs)
            except ConnectionFailure:
                continue
        raise MongoDBConnectionError("Ошибка соединения с MongoDB-сервером")
    return wrapper

@check_mongo_connection
def save_query_info(collection, document: dict):
    return collection.insert_one(document)


@check_mongo_connection
def get_five_most_popular_queries(collection, get_five_most_popular_queries_pipeline):
    return collection.aggregate(get_five_most_popular_queries_pipeline)


@check_mongo_connection
def get_five_last_queries(collection, get_five_last_queries_pipeline):
    return collection.aggregate(get_five_last_queries_pipeline)
