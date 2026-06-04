MYSQL_KEYWORD_SEARCH_QUERY = """
    SELECT flm.film_id, flm.title, flm.release_year flm.description,
           cat.name
    FROM film flm
    JOIN film_category flm_cat ON film.film_id = film_category.film_id
    JOIN category cat ON flm_cat.category_id = cat.category_id
    WHERE film.title = %s
    LIMIT 10 OFFSET %s
"""

MYSQL_GENRE_AND_YEAR_SEARCH_QUERY = """
    SELECT flm.film_id, flm.title, flm.release_year flm.description,
           cat.name
    FROM film flm
    JOIN film_category flm_cat ON film.film_id = film_category.film_id
    JOIN category cat ON flm_cat.category_id = cat.category_id
    WHERE cat.name = %s AND flm.release_year BETWEEN %s AND %s
    LIMIT 10 OFFSET %s
"""

MYSQL_GET_AVAILABLE_GENRES_QUERY = """
    SELECT name
    FROM category
    ORDER BY name
"""

MYSQL_GET_AVAILABLE_YEARS_RANGE_QUERY = """
    SELECT min(release_year) as min_release_year, max(release_year) as max_year
    FROM film
"""

MONGO_GET_FIVE_MOST_POPULAR_QUERIES = [
    {
        "$group": {
            "_id": "$query",
            "searches_number": {"$sum": 1}
        }
    },
    {
        "$sort": {
            "searches_number": -1
        }
    },
    {
        "$limit": 5
    }
]

MONGO_GET_FIVE_LAST_QUERIES = [
    {
        "$sort": {
            "timestamp": -1
        }
    },
    {
        "$limit": 5
    }
]
