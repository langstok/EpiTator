def get_geo_obj(annotation):
    geoname = annotation.geoname
    return {
        "name": geoname['name'],
        "geonameid": geoname['geonameid'],
        "latitude":  geoname['latitude'],
        "longitude": geoname['longitude'],
        'country_code': geoname['country_code'],
        'score': geoname['score'],
        'start': annotation.start,
        'end': annotation.end,
        'text': annotation.text
    }