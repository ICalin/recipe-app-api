#!/bin/sh

set -e

# this line is taking a template file (default.conf.tpl), substituting any environment variable placeholders with their actual values, 
# and then saving the result as the configuration file (default.conf) dynamically configure applications by injecting
# environment-specific values into configuration files during container initialization or application deployment
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
# run nginx in the foreground, the primary thing run by the docker container
nginx -g 'daemon off;'

