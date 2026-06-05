"""CLI layout rendering module for presenting tabular screens and query results using tabulate."""

from tabulate import tabulate


def show_main_menu():
    """
    Render the main navigation menu with available system actions.

    :return: None
    """

    actions = [["[k] / [keyword]: Keyword search"],
               ["[g] / [genre]: Genre and release year search"],
               ["[h] / [history]: Five most recent\nand five most popular queries"],
               ["[e] / [exit]: Exit app"]]
    print(tabulate(actions,
                   headers=["\nWelcome to movie search app!\nSelect an action below\n"],
                   tablefmt="fancy_grid"))


def show_keyword_search_screen():
    """
    Display the header and input instructions for keyword-based search.

    :return: None
    """

    print(tabulate([["Example input:\n\nEnter a keyword: duck"]],
                   headers=[f"\nKeyword search menu\n"],
                   tablefmt="fancy_grid"))


def show_genre_and_years_range_search_screen(genres, years_range):
    """
    Display available filter constraints and usage examples for genre search.

    :param genres: Collection of registered movie genres in the system.
    :param years_range: Systemic minimum and maximum boundary release years.
    :return: None
    """

    genres_and_years = [[f"Available genres:\n{"".join(f"{genre}\n" for genre in genres)}"],
                        [f"Available years:\n{" - ".join(f"{year}" for year in years_range)}"],
                        ["""Example input:
                        
                        Enter a genre: foreign
                        Enter a year range: 2005 2007
                        or
                        Enter a release year a year range: 2006"""]]
    print(tabulate(genres_and_years,
                   headers=[f"\nGenre and release year\nsearch menu\n"],
                   tablefmt="fancy_grid"))


def show_history_screen(five_last_queries, five_most_popular_queries):
    """
    Present comparative statistics tables for recent and frequent queries.

    :param five_last_queries: Iterable collection of the most recent log documents.
    :param five_most_popular_queries: Iterable collection of top aggregated log records.
    :return: None
    """

    formatted_recent_queries = tuple("\n".join(f"{k}: {v}" for k, v in row.items())
                                     for row in five_last_queries)
    formatted_most_popular_queries = tuple("\n".join(f"{k}: {v}" for k, v in row.items())
                                           for row in five_most_popular_queries)
    print(tabulate(list(zip(formatted_recent_queries, formatted_most_popular_queries)),
                    headers=["Five most recent queries: ", "Five most popular queries: "],
                   tablefmt="fancy_grid"))
    print("│ [b] / [back]: Back to menu")
    print("╘═══════════════════════════════════════════════════════════════════════╛")


def show_search_result(rows):
    """
    Render current page movie rows in a grid alongside absolute summary count.

    :param rows: Dataset of movie objects containing technical metadata fields.
    :return: None
    """

    total_rows_count = rows[0]["total_rows_count"]
    clear_rows = [{k: v for k, v in row.items() if k != "total_rows_count"}
                  for row in rows] + [{"id": "","title": "","release_year": "",
                                       "name": "Total rows count:","description": total_rows_count}]
    print(tabulate(clear_rows,
                   headers="keys",
                   maxcolwidths=[None, None, None, None, None, 30],
                   tablefmt="fancy_grid"))
    print("│ [n] / [next]: Next page   [p] / [previous]: Previous page\n│ [b] / [back]: Back to menu")
    print("╘═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╛")