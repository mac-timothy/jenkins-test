# ==========================================================
# Base Image
# ----------------------------------------------------------
# Start from the official Python 3.13 slim image.
#
# Why slim?
# - Smaller image size than the full Python image
# - Faster downloads and deployments
# - Lower storage usage
# - Fewer unnecessary packages (better security)
#
# This image already contains:
# - Linux (Debian Slim)
# - Python 3.13
# - pip
#
# Everything else required by our application will be
# installed in the next steps.
# ==========================================================
FROM python:3.13-slim


# ==========================================================
# Working Directory
# ----------------------------------------------------------
# Create (if it doesn't already exist) and switch to the
# /app directory inside the container.
#
# From this point onwards, every command executes inside
# /app.
#
# Equivalent to running:
#     mkdir -p /app
#     cd /app
#
# Our backend source code will live here.
# ==========================================================
WORKDIR /app


# ==========================================================
# Copy Dependency File
# ----------------------------------------------------------
# Copy ONLY requirements.txt into the container first.
#
# Why?
#
# Docker builds images using layers.
#
# If our application code changes but requirements.txt
# remains the same, Docker can reuse the dependency layer
# instead of reinstalling every package.
#
# This significantly speeds up rebuilds during development
# and CI/CD.
# ==========================================================
COPY requirements.txt .


# ==========================================================
# Install Python Dependencies
# ----------------------------------------------------------
# Install all backend dependencies listed in requirements.txt.
#
# Examples include:
# - FastAPI
# - Uvicorn
# - SQLAlchemy
# - psycopg2
# - python-dotenv
# - pytest
#
# The --no-cache-dir option prevents pip from storing
# downloaded package files, making the final Docker image
# smaller.
#
# This command runs ONLY during docker build.
# ==========================================================
RUN pip install --no-cache-dir -r requirements.txt


# ==========================================================
# Copy Application Source Code
# ----------------------------------------------------------
# Copy everything from the backend project into /app.
#
# This includes:
# - app/
# - tests/
# - assets/
# - pytest.ini
# - .env (if not excluded by .dockerignore)
#
# Since requirements.txt has already been copied and the
# dependencies installed, changing only Python source code
# will not force Docker to reinstall packages.
# ==========================================================
COPY . .


# ==========================================================
# Application Port
# ----------------------------------------------------------
# Inform Docker that this application listens on port 8000.
#
# NOTE:
# This does NOT publish the port to your computer.
#
# The actual port mapping happens when running:
#
# docker run -p 8000:8000 image_name
#
# FastAPI (Uvicorn) listens on this port inside the container.
# ==========================================================
EXPOSE 8000


# ==========================================================
# Default Startup Command
# ----------------------------------------------------------
# Start the FastAPI application using Uvicorn.
#
# app.main:app means:
#
# app        -> app/ directory
# main       -> main.py
# app        -> FastAPI instance
#
# --host 0.0.0.0
# Makes the application accessible from outside the
# container.
#
# --port 8000
# Runs the application on port 8000.
#
# This command executes ONLY when a container is started
# using:
#
# docker run image_name
#
# It is NOT executed during docker build.
# ==========================================================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]