FROM python:3.9-alpine3.13
LABEL maintainer="londonappdeveloper.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# write helper scripts that are run by the docker application
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# create only one image, doesnt create so many layers
# first line creates a new virtual env, not everyone used
# second line upgrade the pip for the virtual env we created
# install the requirements
# 4th line to keep the docker image as lightweight as possible
# add a new user inside the image, is not a good practice to run with the root user

# linux-headers is needed for the WSGI server instalation, it will be deleted after, this is way is in temp files
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

# when we run any python commands to don't have to specify the path
ENV PATH="/scripts:/py/bin:$PATH"

# to run as the user, not as the root 
USER django-user

# the default command that will be executed when a container is run from the image.
CMD ["run.sh"]
