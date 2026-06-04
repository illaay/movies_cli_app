"""Настройки подключения к базе данных с фильмами (MySQL) и базе данных для логирования (MongoDB)"""

import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

MONGO_CONFIG = {
    "uri": os.getenv("MONGO_URI"),
    "database": os.getenv("MONGO_DATABASE"),
    "collection": os.getenv("MONGO_COLLECTION")
}
