FROM python:3.9-alpine3.13
LABEL maintainer="londonappdeveloper.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# create a virtual environment, upgrade pip, and install requirements
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt

# Install additional dependencies for development if DEV=true
ARG DEV=false
RUN if [ $DEV = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi

# Clean up unnecessary files and packages
RUN rm -rf /tmp && \
    apk del .tmp-build-deps

# Create a non-root user for running the application
RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Set the user for subsequent commands
USER django-user

# Set the PATH to the virtual environment
ENV PATH="/py/bin:$PATH"


