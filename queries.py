MYSQL_KEYWORD_SEARCH = """
    SELECT flm.film_id, flm.title, flm.release_year flm.description,
           cat.name
    FROM film flm
    JOIN film_category flm_cat ON film.film_id = film_category.film_id
    JOIN category cat ON flm_cat.category_id = cat.category_id
    WHERE film.title = %s
    LIMIT 10 OFFSET %s
"""

MYSQL_GENRE_AND_YEAR_SEARCH = """
    SELECT flm.film_id, flm.title, flm.release_year flm.description,
           cat.name
    FROM film flm
    JOIN film_category flm_cat ON film.film_id = film_category.film_id
    JOIN category cat ON flm_cat.category_id = cat.category_id
    WHERE cat.name = %s AND flm.release_year BETWEEN %s AND %s
    LIMIT 10 OFFSET %s
"""
