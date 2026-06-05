"""MySQL database client for establishing connections and executing movie lookups."""

import pymysql
from functools import wraps
from pymysql.cursors import DictCursor
from errors import MySQLConnectionError


def create_mysql_connection(config_dict):
    """
    Open a live connection to the MySQL database server.

    :param config_dict: Connection parameters from configuration.
    :return: Configured PyMySQL connection instance.
    """

    return pymysql.connect(**config_dict, cursorclass=DictCursor)


def check_mysql_connection(func):
    """
    Ensure the database connection is active before calling the operation.

    :param func: Database function to be wrapped.
    :return: Protected execution wrapper.
    """

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
    """
    Execute fuzzy text search on movie records with pagination.

    :param connection: Active MySQL database connection instance.
    :param keyword_search_query: Parameterized SQL query string for search.
    :param keyword: Target string to lookup in titles.
    :param offset: Pagination offset boundary for slicing.
    :return: List of matching movie records.
    """

    with connection.cursor() as cursor:
        cursor.execute(keyword_search_query, (f"%{keyword}%", offset))
        result = cursor.fetchall()
    return result


@check_mysql_connection
def search_by_genre_and_year(connection, genre_year_search_query, genre, years: tuple, offset):
    """
    Filter movie records by genre classification and release year span.

    :param connection: Active MySQL database connection instance.
    :param genre_year_search_query: Parameterized SQL query string for filtering.
    :param genre: Target movie genre to filter by.
    :param years: Lower and upper boundaries of the release year.
    :param offset: Pagination offset boundary for slicing.
    :return: List of filtered movie records.
    """

    with connection.cursor() as cursor:
        cursor.execute(genre_year_search_query, (genre, *years, offset))
        result = cursor.fetchall()
    return result


@check_mysql_connection
def get_available_genres(connection, available_genres_query):
    """
    Retrieve all valid movie categories stored in the system.

    :param connection: Active MySQL database connection instance.
    :param available_genres_query: SQL query string to pull unique genres.
    :return: List of available genre dictionaries.
    """

    with connection.cursor() as cursor:
        cursor.execute(available_genres_query)
        result = cursor.fetchall()
    return result


@check_mysql_connection
def get_available_years_range(connection, available_years_range_query):
    """
    Fetch systemic lower and upper release year boundaries.

    :param connection: Active MySQL database connection instance.
    :param available_years_range_query: SQL query string to extract year boundaries.
    :return: List containing dictionary with min and max years.
    """

    with connection.cursor() as cursor:
        cursor.execute(available_years_range_query)
        result = cursor.fetchall()
    return result