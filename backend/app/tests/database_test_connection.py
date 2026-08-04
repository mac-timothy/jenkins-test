from app.database import engine


def test_database_connection():

    try:
        with engine.connect():
            print("Database connection successful")

    except Exception as e:
        print(f"Database connection failed: {e}")
        raise