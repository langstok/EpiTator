# (from repository root) $ docker build . -f docker/processor/Dockerfile -t putssander/nlpflow-epitator:latest
FROM springcloud/openjdk:latest

# Install the required packages
RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential \
    libssl-dev \
    git \
    curl && \
    apt-get -q clean -y && rm -rf /var/lib/apt/lists/* && rm -f /var/cache/apt/*.bin

# run SCDF with Kafka
RUN pip3 install kafka-python

WORKDIR /app/
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY ./epitator/importers /app/epitator/importers
COPY ./epitator/__init__.py ./epitator/get_database_connection.py ./epitator/version.py  ./epitator/utils.py /app/epitator/

ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app/epitator
RUN python3 -m epitator.importers.import_geonames

WORKDIR /app/
COPY ./ / /app/

ENTRYPOINT ["python3", "/app/epitator/processor/python_processor.py", "$@", "--"]
