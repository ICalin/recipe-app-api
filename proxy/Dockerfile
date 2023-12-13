# it runs with root privilege
# it needs only to run it and handle requests from a specific directory
FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="calin.com"

# store the conf in the docker image in the location /etc/nginx/default/conf.tpl
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
# same as before
COPY ./uwsgi_params /etc/nginx/uwsgi_params
#same as before
COPY ./run.sh /run.sh


ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

# to set up the image
USER root


RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]