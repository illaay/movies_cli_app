def show_main_menu():
    print(f"Главное меню. Выбор пункта:",
          "1. Поиск по названию",
          "2. Поиск по жанру и году выпуска",
          "3. История",
          "4. Выход", sep="\n")


def show_keyword_search_screen():
    print("Поиск по ключевому слову")


def show_keyword_search_result(rows): # вынести в отдельную функцию с show_genre_and_years_range_result
    print("Результат поиска по ключевому слову:")
    if rows:
        for row in rows:
            print(row)
    else:
        print("Запросов больше нет")


def show_genre_and_years_range_screen(genres, years_range):
    print("Поиск по жанру и году",
          "Доступные жанры: ",
          *genres,
          "Доступные годы: ",
          years_range, sep="\n")


def show_genre_and_years_range_result(rows):  # вынести в отдельную функцию с show_keyword_search_result
    print("Результат поиска по жанру и году:")  # print("Результат поиска по {search_type}")
    if rows:
        for row in rows:
            print(row)
    else:
        print("Запросов больше нет")


def show_history_screen(five_last_queries, five_most_popular_queries):
    print("5 последних запросов: ",
          *five_last_queries,
          "5 самых популярных запросов: ",
          *five_most_popular_queries, sep="\n")
