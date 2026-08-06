"""
Database Configuration Module
=============================

Responsible for:

1. Detecting the current application environment.
2. Loading the correct environment variables file.
3. Selecting the correct database credentials.
4. Creating the PostgreSQL database connection.
5. Creating SQLAlchemy database sessions.
6. Providing database sessions to FastAPI routes.

Environment files:

.env
    Used for normal application development.

    Contains:
        DB_USER
        DB_PASSWORD
        DB_HOST
        DB_PORT
        DB_NAME


.env.test
    Used during automated testing with pytest/Jenkins.

    Contains:
        TEST_DB_USER
        TEST_DB_PASSWORD
        TEST_DB_HOST
        TEST_DB_PORT
        TEST_DB_NAME


Environment flow:

Development:

    Application
        |
        |
        v
    ENVIRONMENT=development
        |
        |
        v
    Load .env
        |
        |
        v
    Connect to development database


Testing:

    Jenkins
        |
        |
        v
    ENVIRONMENT=test
        |
        |
        v
    Load .env.test
        |
        |
        v
    Connect to testing database


The separation prevents automated tests from modifying
the development or production database.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os



# ---------------------------------------------------------
# Determine application environment
#
# The application checks the ENVIRONMENT variable.
#
# If it does not exist, the default environment is:
#
#     development
#
#
# Jenkins will provide:
#
#     ENVIRONMENT=test
#
# when running automated tests.
#
# This value decides which environment file is loaded.
# ---------------------------------------------------------

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)



# ---------------------------------------------------------
# Load environment configuration
#
# Development:
#
#     Loads .env
#
# Testing:
#
#     Loads .env.test
#
# load_dotenv() reads variables from the file and
# makes them available through os.getenv()
# ---------------------------------------------------------

if ENVIRONMENT == "test":

    # Load testing database configuration
    load_dotenv(".env.test")

else:

    # Load development database configuration
    load_dotenv(".env")



# ---------------------------------------------------------
# Load database credentials
#
# Different environments use different variable names.
#
# Development database:
#
#     DB_USER
#     DB_PASSWORD
#     DB_HOST
#     DB_PORT
#     DB_NAME
#
#
# Testing database:
#
#     TEST_DB_USER
#     TEST_DB_PASSWORD
#     TEST_DB_HOST
#     TEST_DB_PORT
#     TEST_DB_NAME
#
# ---------------------------------------------------------

if ENVIRONMENT == "test":

    DB_USER = os.getenv("TEST_DB_USER")
    DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
    DB_HOST = os.getenv("TEST_DB_HOST")
    DB_PORT = os.getenv("TEST_DB_PORT")
    DB_NAME = os.getenv("TEST_DB_NAME")


else:

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")



# ---------------------------------------------------------
# Validate database configuration
#
# Before connecting to PostgreSQL, confirm that all
# required variables exist.
#
# Without this check, SQLAlchemy may produce unclear
# errors such as:
#
#     invalid literal for int() with base 10: 'None'
#
# This provides an immediate and understandable error.
# ---------------------------------------------------------

required_variables = {

    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME

}


missing_variables = [

    key
    for key, value in required_variables.items()
    if value is None

]


if missing_variables:

    raise RuntimeError(
        f"Missing database configuration: {missing_variables}"
    )



# ---------------------------------------------------------
# Create PostgreSQL connection URL
#
# SQLAlchemy requires a connection string to communicate
# with PostgreSQL.
#
#
# Format:
#
# postgresql+driver://user:password@host:port/database
#
#
# psycopg2:
#
#     PostgreSQL driver used by SQLAlchemy.
#
#
# sslmode=require:
#
#     Forces encrypted communication.
#
#     Required when connecting to Supabase PostgreSQL.
#
# ---------------------------------------------------------

DATABASE_URL = (

    f"postgresql+psycopg2://"
    f"{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
    "?sslmode=require"

)



# ---------------------------------------------------------
# Create SQLAlchemy Engine
#
# The engine is the main connection manager between
# the FastAPI application and PostgreSQL.
#
# It manages:
#
# - database connections
# - connection pooling
# - communication with PostgreSQL
#
# All database operations go through the engine.
# ---------------------------------------------------------

engine = create_engine(
    DATABASE_URL
)



# ---------------------------------------------------------
# Create Database Session Factory
#
# A session represents a temporary connection to the
# database used for performing operations.
#
# Examples:
#
# - Reading users
# - Creating products
# - Updating records
# - Deleting data
#
#
# Each API request receives its own session.
# ---------------------------------------------------------

SessionLocal = sessionmaker(

    autocommit=False,
    autoflush=False,
    bind=engine

)



# ---------------------------------------------------------
# Create SQLAlchemy Base Class
#
# Database models inherit from this class.
#
# Example:
#
# class User(Base):
#     __tablename__ = "users"
#
#
# SQLAlchemy uses this class to understand database
# table definitions.
# ---------------------------------------------------------

Base = declarative_base()



# ---------------------------------------------------------
# FastAPI Database Dependency
#
# This function provides database access to API routes.
#
#
# Request flow:
#
# User Request
#       |
#       v
# FastAPI Endpoint
#       |
#       v
# get_db()
#       |
#       v
# Open database session
#       |
#       v
# Perform database operations
#       |
#       v
# Close session
#
#
# The finally block guarantees that the connection is
# closed even if an error occurs.
# ---------------------------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()