import psycopg

from app.core.config import settings
from sqlalchemy.engine import make_url


def test_connection():
    """Test PostgreSQL authentication from Windows."""

    url = make_url(settings.database_url)

    with psycopg.connect(
        host=url.host,
        port=url.port,
        dbname=url.database,
        user=url.username,
        password=url.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("Connection successful:", cursor.fetchone()[0])


if __name__ == "__main__":
    test_connection()