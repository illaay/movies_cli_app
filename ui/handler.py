"""Application controller module that coordinates user navigation, search flows, and database interactions."""

import config
import log_utils
from ui import interface
from db import queries
from db import mysql_client
from db import mongo_client
from datetime import datetime
from errors import ApplicationCrushError


@log_utils.logger
def keyword_search(connection, collection, search_query):
    """
    Manage the movie search flow by a user-provided keyword with pagination.

    :param connection: Active MySQL database connection instance.
    :param collection: Active MongoDB history collection instance.
    :param search_query: Parameterized SQL query string for keyword lookup.
    :return: None
    """

    interface.show_keyword_search_screen()
    while True:
        user_keyword = input("│ Enter a keyword: ").strip()
        if user_keyword:
            break
        print("Query is empty, please try again")

    page_number = 1
    search_cache = {}

    while True:
        offset = (page_number - 1) * 10

        if page_number in search_cache:
            search_result = search_cache[page_number]
        else:
            search_result = mysql_client.search_by_keyword(connection, search_query, user_keyword, offset)
            search_cache[page_number] = search_result
        interface.show_search_result(search_result)

        if search_result:
            total_rows_count = search_result[0]["total_rows_count"]
        else:
            total_rows_count = 0

        is_first_page = True if page_number == 1 else False
        is_last_page = True if len(search_result) < 10 else False

        while True:
            action = input("│ Enter next action: ").strip().lower()

            if action in ("n", "next") and not is_last_page:
                page_number += 1
            elif action in ("p", "previous") and not is_first_page:
                page_number -= 1
            elif action in ("b", "back"):
                history_doc = {
                    "type": "keyword",
                    "query_data": f"{user_keyword}",
                    "total_rows_count": total_rows_count,
                    "timestamp": datetime.now()
                }
                mongo_client.save_query_info(collection, history_doc)
                return
            else:
                print("Incorrect input, please try again")
                continue
            break


@log_utils.logger
def genre_and_year_search(connection, collection, search_query, get_genres_query, get_available_years_query):
    """
    Filter movie records by selecting a valid genre and a specific release year range.

    :param connection: Active MySQL database connection instance.
    :param collection: Active MongoDB history collection instance.
    :param search_query: Parameterized SQL query string for genre and year filtering.
    :param get_genres_query: SQL query string to fetch available genres.
    :param get_available_years_query: SQL query string to fetch systemic min and max years.
    :return: None
    """

    genres_tuple = tuple(row["name"] for row in mysql_client.get_available_genres(connection, get_genres_query))
    available_years = mysql_client.get_available_years_range(connection, get_available_years_query)
    years_tuple = tuple((available_years[0]["min_release_year"], available_years[0]["max_release_year"]))
    del available_years
    interface.show_genre_and_years_range_search_screen(genres_tuple, years_tuple)

    while True:
        user_genre = input("│ Enter a genre: ").strip().title()
        if user_genre in genres_tuple:
            break
        print("Incorrect input, please try again")

    while True:
        user_years = input("│ Enter a release year a year range: ").strip().split()

        try:
            user_years = tuple(int(year) for year in user_years)
        except ValueError:
            print("Incorrect input, please try again")
            continue

        if not all(years_tuple[0] <= _ <= years_tuple[1] for _ in user_years):
            print(f"Years must be within range, please try again")
            continue

        if not 1 <= len(user_years) <= 2:
            print("Expected one or two years, please try again")
            continue

        if len(user_years) == 1:
            user_years = tuple((user_years[0], user_years[0]))

        if not user_years[0] <= user_years[1]:
            print("The second year must be greater than the first, please try again.")
            continue

        break

    page_number = 1
    search_cache = {}

    while True:
        offset = (page_number - 1) * 10

        if page_number in search_cache:
            search_result = search_cache[page_number]
        else:
            search_result = mysql_client.search_by_genre_and_year(connection, search_query, user_genre, user_years, offset)
            search_cache[page_number] = search_result
        interface.show_search_result(search_result)

        if search_result:
            total_rows_count = search_result[0]["total_rows_count"]
        else:
            total_rows_count = 0

        is_first_page = True if page_number == 1 else False
        is_last_page = True if len(search_result) < 10 else False

        while True:
            action = input("│ Enter next action: ").strip().lower()

            if action in ("n", "next") and not is_last_page:
                page_number += 1
            elif action in ("p", "previous") and not is_first_page:
                page_number -= 1
            elif action in ("b", "back"):
                history_doc = {
                    "type": "genre_and_year",
                    "query_data": f"{user_genre} {user_years}",
                    "total_rows_count": total_rows_count,
                    "timestamp": datetime.now()
                }
                mongo_client.save_query_info(collection, history_doc)
                return
            else:
                print("Incorrect input, please try again")
                continue
            break


@log_utils.logger
def five_last_and_popular_queries(collection, five_last_queries_query, five_most_popular_queries_query):
    """
    Retrieve and present recent user search logs and top frequent aggregation statistics.

    :param collection: Active MongoDB history collection instance.
    :param five_last_queries_query: MongoDB aggregation pipeline for recent logs.
    :param five_most_popular_queries_query: MongoDB aggregation pipeline for popularity stats.
    :return: None
    """

    five_last_queries = tuple(mongo_client.get_five_last_queries(collection, five_last_queries_query))
    five_most_popular_queries = tuple(mongo_client.get_five_most_popular_queries(collection, five_most_popular_queries_query))
    interface.show_history_screen(five_last_queries, five_most_popular_queries)

    while True:
        action = input("│ Enter next action: ")
        if action == "b":
            return
        print("Incorrect input, please try again")



def run_app():
    mysql_conn = mysql_client.create_mysql_connection(config.MYSQL_CONFIG)
    mongo_coll = mongo_client.create_mongo_connection(config.MONGO_CONFIG)
    log_utils.log_info("Application launched and databases connected successfully")

    try:
        while True:
            interface.show_main_menu()
            user_action_selection = input("│ Enter an action: ")

            match user_action_selection:
                case "k" | "keyword":
                    keyword_search(mysql_conn,
                                   mongo_coll,
                                   queries.MYSQL_KEYWORD_SEARCH_QUERY)
                case "g" | "genre":
                    genre_and_year_search(mysql_conn,
                                          mongo_coll,
                                          queries.MYSQL_GENRE_AND_YEAR_SEARCH_QUERY,
                                          queries.MYSQL_GET_AVAILABLE_GENRES_QUERY,
                                          queries.MYSQL_GET_AVAILABLE_YEARS_RANGE_QUERY)
                case "h" | "history":
                    five_last_and_popular_queries(mongo_coll,
                                                  queries.MONGO_GET_FIVE_LAST_QUERIES,
                                                  queries.MONGO_GET_FIVE_MOST_POPULAR_QUERIES)
                case "e" | "exit":
                    break
                case _:
                    print("Incorrect input, please try again")
    except Exception as e:
        log_utils.log_critical("Critical application failure occurred")
        mysql_conn.close()
        raise ApplicationCrushError("A critical error caused the application to terminate") from e