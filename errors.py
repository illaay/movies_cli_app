class MySQLConnectionError(ConnectionError):
    """Raised when the application fails to connect or communicate with the MySQL server."""

    pass


class MongoDBConnectionError(ConnectionError):
    """Raised when the application fails to connect or communicate with the MongoDB server."""

    pass


class ApplicationCrushError(Exception):
    """Raised when an unrecoverable fatal failure forces the application to terminate."""

    pass
