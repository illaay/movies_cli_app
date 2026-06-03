import pymysql
from functools import wraps
from pymysql.cursors import DictCursor
from errors import MySQLConnectionError


def create_mysql_connection(config_dict):
    return pymysql.connect(**config_dict, cursorclass=DictCursor)


def check_mysql_connection(func):
    @wraps(func)
    def wrapper(connection, *args, **kwargs):
        try:
            connection.ping(reconnect=True)
        except (pymysql.OperationalError, pymysql.InterfaceError):
            raise MySQLConnectionError("Ошибка соединения c MySQL-сервером")
        return func(connection, *args, **kwargs)
    return wrapper

@check_mysql_connection
def search_by_keyword(connection, keyword_search_query, keyword, offset):
    with connection.cursor() as cursor:
        cursor.execute(keyword_search_query, (keyword, offset))
        result = cursor.fetchall()
    return result

@check_mysql_connection
def search_by_genre_and_year(connection, genre_year_search_query, genre, years: tuple, offset):
    with connection.cursor() as cursor:
        cursor.execute(genre_year_search_query, (genre, *years, offset))
        result = cursor.fetchall()
    return result
