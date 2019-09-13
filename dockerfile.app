ARG PYTHON_VERSION=3.7
FROM tiangolo/uwsgi-nginx-flask:python${PYTHON_VERSION}

RUN adduser --disabled-login --gecos '' apprunner
RUN mkdir -p /home/apprunner/.aws
RUN touch /home/apprunner/.aws/credentials
RUN touch /home/apprunner/.aws/config
RUN chown -R apprunner:apprunner /home/apprunner/.aws

ENV FLASK_APP /app/unicorn.py
ENV STATIC_URL /app/app/static

ADD requirements.txt /app/requirements.txt
RUN sed '/^uWSGI/ d' < /app/requirements.txt > /app/requirements_filtered.txt
WORKDIR /app/
RUN pip install -r requirements_filtered.txt
RUN pip install urlparser secretcli

RUN apt-get update \
 && apt-get install -y -f netcat \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD ./docker/app/uwsgi.ini /app/uwsgi.ini
ADD ./docker/app/prestart.sh /app/prestart.sh
ADD ./docker/app/nginx_overrides.conf /etc/nginx/conf.d/nginx_overrides.conf


ADD ./migrations/ /app/migrations
ADD ./app/ /app/app
ADD ./manage.py /app/manage.py
ADD ./unicorn.py /app/unicorn.py
