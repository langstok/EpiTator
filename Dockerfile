FROM tiangolo/uwsgi-nginx-flask:python3.7
MAINTAINER Sander Puts

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./epitator/importers /app/epitator/importers
COPY ./epitator/__init__.py ./epitator/get_database_connection.py ./epitator/version.py  ./epitator/utils.py /app/epitator/

WORKDIR /app/epitator
RUN python -m epitator.importers.import_geonames

COPY . / /app/
WORKDIR /app


COPY ./epitator/serve.py /app/epitator/serve.py

# debug only
RUN pip install flask

ENV OPTIONAL_ARGS=''
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV AM_I_IN_A_DOCKER_CONTAINER Yes


ENV LISTEN_PORT 8080
