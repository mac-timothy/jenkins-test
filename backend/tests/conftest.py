"""
Pytest configuration file.

Responsibilities:

1. Load test environment variables.
2. Connect to dedicated test database.
3. Protect production database.
4. Replace FastAPI database dependency.
5. Provide API client.
6. Clean database before every test.
7. Create reusable test users.


Testing lifecycle:

pytest starts

      |

Load fixtures

      |

Connect test database

      |

Clean database

      |

Create test data

      |

Run tests

      |

Generate report

"""



import os

import uuid


import pytest


from dotenv import load_dotenv


from sqlalchemy import create_engine, text


from sqlalchemy.orm import sessionmaker


from fastapi.testclient import TestClient



from app.main import app

from app.database.database import Base, get_db





# =====================================================
# Load test environment
# =====================================================


load_dotenv(".env.test")





# =====================================================
# Safety check
#
# Prevent accidental production testing.
# =====================================================


if os.getenv("ENVIRONMENT") != "test":

    raise Exception(

        """
        Tests stopped.

        Add:

        ENVIRONMENT=test

        to .env.test

        """

    )





# =====================================================
# Test database URL
# =====================================================


TEST_DATABASE_URL = (

    f"postgresql://"

    f"{os.getenv('TEST_DB_USER')}:"

    f"{os.getenv('TEST_DB_PASSWORD')}@"

    f"{os.getenv('TEST_DB_HOST')}:"

    f"{os.getenv('TEST_DB_PORT')}/"

    f"{os.getenv('TEST_DB_NAME')}"

)





# =====================================================
# Database engine
# =====================================================


engine = create_engine(

    TEST_DATABASE_URL

)





# =====================================================
# Database session factory
# =====================================================


TestingSessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)





# =====================================================
# Create database tables
# =====================================================


Base.metadata.create_all(

    bind=engine

)





# =====================================================
# Replace application database
#
# App database  ---> Production
#
# Test database ---> During pytest
# =====================================================


def override_get_db():


    database = TestingSessionLocal()


    try:

        yield database


    finally:

        database.close()





app.dependency_overrides[get_db] = override_get_db





# =====================================================
# Clean database before every test
#
# This prevents:
#
# duplicate emails
# old users
# test dependency
#
# =====================================================


@pytest.fixture(autouse=True)

def clean_database():


    database = TestingSessionLocal()


    try:


        database.execute(

            text(

                """

                TRUNCATE TABLE users

                RESTART IDENTITY

                CASCADE

                """

            )

        )


        database.commit()



    finally:


        database.close()





# =====================================================
# FastAPI test client
# =====================================================


@pytest.fixture

def client():


    with TestClient(app) as test_client:


        yield test_client





# =====================================================
# Direct database access
# =====================================================


@pytest.fixture

def db():


    database = TestingSessionLocal()


    try:


        yield database



    finally:


        database.rollback()

        database.close()





# =====================================================
# User creation helper
#
# Username:
# controlled
#
# Password:
# controlled
#
# Email:
# automatically generated
#
# =====================================================


@pytest.fixture

def create_user(client):


    def _create_user(

        username,

        password,

        email=None

    ):


        if email is None:


            email = (

                f"user_{uuid.uuid4()}@test.com"

            )





        user = {


            "username": username,


            "email": email,


            "password": password

        }





        response = client.post(

            "/auth/signup",

            json=user

        )





        assert response.status_code == 200, (

            f"""

            User creation failed.


            Status:

            {response.status_code}


            Response:

            {response.json()}

            """

        )





        return user





    return _create_user