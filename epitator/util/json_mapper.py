def get_geo_obj(annotation):
    geoname_json = {
        "name": annotation.geoname.name,
        "geonameid": annotation.geoname.geonameid,
        "latitude":  annotation.geoname.latitude,
        "longitude": annotation.geoname.longitude,
        'country_code': annotation.geoname.country_code,
        'score': annotation.geoname.score,
        'start': annotation.start,
        'end': annotation.end,
        'text': annotation.text
    }
    return geoname_json
