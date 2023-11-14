FROM python:3.9-alpine3.13
LABEL maintainer="londonappdeveloper.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# create only one image, doesnt create so many layers
# first line creates a new virtual env, not everyone used
# second line upgrade the pip for the virtual env we created
# install the requirements
# 4th line to keep the docker image as lightweight as possible
# add a new user inside the image, is not a good practice to run with the root user

ARG DEV=false

RUN python -m venv /py && \ 
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && \
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

# when we run any python commands to don't have to specify the path
ENV PATH="/py/bin:$PATH"

# to run as the user, not as the root 
USER django-user
