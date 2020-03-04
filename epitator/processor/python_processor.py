#!/usr/bin/env python
import json
import logging
import os

from epitator.geoname_annotator import GeonameAnnotator

from epitator.annodoc import AnnoDoc
from kafka import KafkaConsumer, KafkaProducer

from util.http_status_server import HttpHealthServer
from util.task_args import get_kafka_binder_brokers, get_input_channel, get_output_channel

from epitator.util.json_mapper import get_geo_obj

logging.basicConfig()
logger = logging.getLogger('python-processor')
logger.setLevel(level=logging.INFO)

print("ENV", os.environ, flush=True)

consumer = KafkaConsumer(get_input_channel(), bootstrap_servers=[get_kafka_binder_brokers()])
producer = KafkaProducer(bootstrap_servers=[get_kafka_binder_brokers()])
HttpHealthServer.run_thread()

while True:
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        text = data["json-nlp"]["documents"][0]["text"]
        logger.info("In text: %s", text)
        try:
            doc = AnnoDoc(text=text)
            doc.add_tiers(GeonameAnnotator())
            annotations = doc.tiers["geonames"].spans
            logger.info("annotations %s", str(annotations))
            results = []
            for annotation in annotations:
                results.append(get_geo_obj(annotation))
            logger.info("results %s", str(results))
            data['epitator'] = {
                'geoname-annotator': results
            }
            logger.info("epitator %s", str(data['epitator']))
        except Exception as e:
            logger.error('error', e)

        producer.send(get_output_channel(), json.dumps(data).encode('utf-8'))


