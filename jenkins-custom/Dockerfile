# =====================================================
# Custom Jenkins image
#
# Base:
# Jenkins with Java 21
#
# We add:
# - Python
# - pip
# - virtual environment support
# - Git tools
#
# This allows Jenkins pipelines to run
# Python projects and pytest.
# =====================================================


FROM jenkins/jenkins:lts-jdk21



# Switch to root because
# installing packages requires admin permissions

USER root



# Update package list
# Install Python tooling

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git && \
    rm -rf /var/lib/apt/lists/*



# Return to Jenkins user
#
# Jenkins should not run as root.

USER jenkins