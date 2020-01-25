import logging

from flask import Flask, jsonify, request
import json

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


from epitator.annotator import AnnoDoc
from epitator.geoname_annotator import GeonameAnnotator

geonameAnnotator = GeonameAnnotator()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

@app.route('/api/geoname', methods=['GET', 'POST'])
def process_geoname():
    data = {}
    if request.method == 'GET':
        if 'text' not in request.url:
                raise ValueError('You need to request param "text"')
        data['text'] = request.args.get('text')
    else:
        data = request.get_json(silent=True)
    doc = AnnoDoc(str(data))
    doc.add_tiers(geonameAnnotator)
    annotations = doc.tiers["geonames"].spans
    results = []
    for annotation in annotations:
        geoname = annotation.geoname

        results.append({
            "name": geoname['name'],
            "geonameid": geoname['geonameid'],
            "latitude":  geoname['latitude'],
            "longitude": geoname['longitude'],
            'country_code': geoname['country_code']
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=False, port=8080, host='0.0.0.0')
