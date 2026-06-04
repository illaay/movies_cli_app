import config
from ui import interface
from db import queries
from db import mysql_client
from db import mongo_client
from datetime import datetime


def keyword_search(connection, collection, search_query):
    interface.show_keyword_search_screen()
    while True:
        user_keyword = input("Введите ключевое слово: ").strip()
        if user_keyword:
            break
        print("Запрос пуст, повторите попытку")

    page_number = 1
    search_cache = {}

    while True:
        offset = (page_number - 1) * 10

        # если в кэш сохранен результат поиска - берем данные оттуда
        # иначе делаем новый запрос и сохраняем в кэш
        # после условия отображаем результат
        if page_number in search_cache:
            search_result = search_cache[page_number]
        else:
            search_result = mysql_client.search_by_keyword(connection, search_query, user_keyword, offset)
            search_cache[page_number] = search_result
        interface.show_keyword_search_result(search_result)

        if search_result:
            total_rows_count = search_result[0]["total_rows_count"]
        else:
            total_rows_count = 0

        is_first_page = True if page_number == 1 else False
        is_last_page = True if len(search_result) < 10 else False

        while True:
            print(f"{"" if is_last_page else "[n] следующая страница"}")
            print(f"{"" if is_first_page else "[p] предыдущая страница"}")
            print("[b] выход в меню")
            action = input("Введите следующее действие: ").strip()

            if action == "n" and not is_last_page:
                page_number += 1
            elif action == "p" and not is_first_page:
                page_number -= 1
            elif action == "b":
                history_doc = {
                    "type": "keyword",
                    "query_data": f"{user_keyword }",
                    "total_rows_count": total_rows_count,
                    "timestamp": datetime.now()
                }
                mongo_client.save_query_info(collection, history_doc)
                return
            else:
                print("Ошибка ввода, повторите попытку")
                continue
            break


def genre_and_year_search(connection, collection, search_query, get_genres_query, get_available_years_query):

    genres_tuple = tuple(row["name"] for row in mysql_client.get_available_genres(connection, get_genres_query))
    available_years = mysql_client.get_available_years_range(connection, get_available_years_query)
    years_tuple = tuple((available_years[0]["min_release_year"], available_years[0]["max_release_year"]))
    del available_years
    interface.show_genre_and_years_range_screen(genres_tuple, years_tuple)

    while True:
        user_genre = input("Введите жанр: ").strip().title()
        if user_genre in genres_tuple:
            break
        print("Запрос пуст, повторите попытку")

    while True:
        user_years = input("Введите два года через пробел (диапазон): ").strip().split()

        try:
            user_years = tuple(int(year) for year in user_years)
        except ValueError:
            print("Некорректный ввод, повторите попытку")
            continue

        if not all(years_tuple[0] <= _ <= years_tuple[1] for _ in user_years):
            print(f"Годы должен попадать в указанный диапазон, повторите попытку")
            continue

        if not 1 <= len(user_years) <= 2:
            print("Ожидается один или два года, повторите попытку")
            continue

        if len(user_years) == 1:
            user_years = tuple((user_years[0], user_years[0]))
            continue

        if not user_years[0] <= user_years[1]:
            print("Второй указанный год должен быть больше первого, повторите попытку")
            continue

        break

    page_number = 1
    search_cache = {}

    while True:
        offset = (page_number - 1) * 10

        # если в кэш сохранен результат поиска - берем данные оттуда
        # иначе делаем новый запрос и сохраняем в кэш
        # после условия отображаем результат
        if page_number in search_cache:
            search_result = search_cache[page_number]
        else:
            search_result = mysql_client.search_by_genre_and_year(connection, search_query, user_genre, user_years, offset)
            search_cache[page_number] = search_result
        interface.show_genre_and_years_range_result(search_result)

        if search_result:
            total_rows_count = search_result[0]["total_rows_count"]
        else:
            total_rows_count = 0

        is_first_page = True if page_number == 1 else False
        is_last_page = True if len(search_result) < 10 else False

        while True:
            print(f"{"" if is_last_page else "[n] следующая страница"}")
            print(f"{"" if is_first_page else "[p] предыдущая страница"}")
            print("[b] выход в меню")
            action = input("Введите следующее действие: ")

            if action == "n" and not is_last_page:
                page_number += 1
            elif action == "p" and not is_first_page:
                page_number -= 1
            elif action == "b":
                history_doc = {
                    "type": "genre_and_year",
                    "query_data": f"{user_genre} {user_years}",
                    "total_rows_count": total_rows_count,
                    "timestamp": datetime.now()
                }
                mongo_client.save_query_info(collection, history_doc)
                return
            else:
                print("Ошибка ввода, введите заново")
                continue
            break


def five_last_and_popular_queries(collection, five_last_queries_query, five_most_popular_queries_query):

    five_last_queries = tuple(mongo_client.get_five_last_queries(collection, five_last_queries_query))
    five_most_popular_queries = tuple(mongo_client.get_five_most_popular_queries(collection, five_most_popular_queries_query))
    interface.show_history_screen(five_last_queries, five_most_popular_queries)

    while True:
        action = input("[b] выход в меню: ")
        if action == "b":
            return
        print("Ошибка ввода, введите заново")



def run_app():
    mysql_conn = mysql_client.create_mysql_connection(config.MYSQL_CONFIG)
    mongo_coll = mongo_client.create_mongo_connection(config.MONGO_CONFIG)
    # временный try-except для отслеживания неожиданных ошибок
    # потом надо убрать, заменить на логгер
    try:
        while True:
            interface.show_main_menu()
            user_action_selection = int(input("Выберите действие (1-4): "))
            match user_action_selection:
                case 1:
                    keyword_search(mysql_conn,
                                   mongo_coll,
                                   queries.MYSQL_KEYWORD_SEARCH_QUERY)
                case 2:
                    genre_and_year_search(mysql_conn,
                                          mongo_coll,
                                          queries.MYSQL_GENRE_AND_YEAR_SEARCH_QUERY,
                                          queries.MYSQL_GET_AVAILABLE_GENRES_QUERY,
                                          queries.MYSQL_GET_AVAILABLE_YEARS_RANGE_QUERY)
                case 3:
                    five_last_and_popular_queries(mongo_coll,
                                                  queries.MONGO_GET_FIVE_LAST_QUERIES,
                                                  queries.MONGO_GET_FIVE_MOST_POPULAR_QUERIES)
                case 4:
                    break
    except Exception as e:
        mysql_conn.close()
        raise Exception from e