MYSQL_KEYWORD_SEARCH_QUERY = f"""
    SELECT ROW_NUMBER() OVER (ORDER BY flm.film_id) as id,
           flm.film_id, flm.title, flm.release_year, cat.name, flm.description,
           COUNT(*) OVER () total_rows_count
    FROM film flm
    JOIN film_category flm_cat ON flm.film_id = flm_cat.film_id
    JOIN category cat ON flm_cat.category_id = cat.category_id
    WHERE flm.title LIKE %s
    ORDER BY id
    LIMIT 10 OFFSET %s
"""

MYSQL_GENRE_AND_YEAR_SEARCH_QUERY = """
    SELECT ROW_NUMBER() OVER (ORDER BY flm.film_id) as id,
           flm.film_id, flm.title, flm.release_year, cat.name, flm.description,
           COUNT(*) OVER () total_rows_count
    FROM film flm
    JOIN film_category flm_cat ON flm.film_id = flm_cat.film_id
    JOIN category cat ON flm_cat.category_id = cat.category_id
    WHERE cat.name = %s AND flm.release_year BETWEEN %s AND %s
    ORDER BY id
    LIMIT 10 OFFSET %s
"""

MYSQL_GET_AVAILABLE_GENRES_QUERY = """
    SELECT name
    FROM category
    ORDER BY name
"""

MYSQL_GET_AVAILABLE_YEARS_RANGE_QUERY = """
    SELECT MIN(release_year) AS min_release_year, MAX(release_year) as max_release_year
    FROM film
"""

MONGO_GET_FIVE_LAST_QUERIES = [
    {
        "$sort": {
            "timestamp": -1
        }
    },
    {
        "$limit": 5
    },
    {
        "$project" :{"_id": 0}
    }
]

MONGO_GET_FIVE_MOST_POPULAR_QUERIES = [
    {
        "$group": {
            "_id": "$query_data",
            "type": {"$first": "$type"},
            "total_rows_count": {"$first": "$total_rows_count"},
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
