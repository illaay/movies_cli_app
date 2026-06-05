"""MongoDB client module for managing connections, saving logs, and executing analytics aggregation."""

import pymongo
from functools import wraps
from pymongo.errors import ConnectionFailure
from errors import MongoDBConnectionError


def create_mongo_connection(config_dict):
    """
    Establish a connection and verify active link with MongoDB.

    :param config_dict: Connection boundaries from environment parameters.
    :return: Target database collection collection instance.
    """

    try:
        client = pymongo.MongoClient(config_dict["uri"])
        client.admin.command("ping")
        return client[config_dict["database"]][config_dict["collection"]]
    except ConnectionFailure:
        raise MongoDBConnectionError("Ошибка подключения к MongoDB-серверу")


def check_mongo_connection(func):
    """
    Ensure the database connection is active via double execution attempt.

    :param func: Wrapped MongoDB function.
    :return: Protected execution wrapper.
    """

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
    """
    Insert a processed query document record into history logs.

    :param collection: Target MongoDB database collection collection instance.
    :param document: Generated information payload describing user request.
    :return: Insertion transaction response details.
    """

    return collection.insert_one(document)


@check_mongo_connection
def get_five_last_queries(collection, get_five_last_queries_pipeline):
    """
    Fetch five most recent search requests from collection logs.

    :param collection: Target MongoDB database collection collection instance.
    :param get_five_last_queries_pipeline: Processing lookup pipeline commands.
    :return: Command execution database search result iterator.
    """

    return collection.aggregate(get_five_last_queries_pipeline)


@check_mongo_connection
def get_five_most_popular_queries(collection, get_five_most_popular_queries_pipeline):
    """
    Aggregate and retrieve top five most frequent lookup requests.

    :param collection: Target MongoDB database collection collection instance.
    :param get_five_most_popular_queries_pipeline: Data structuring aggregate parameters commands.
    :return: Command execution database search result iterator.
    """

    return collection.aggregate(get_five_most_popular_queries_pipeline)
