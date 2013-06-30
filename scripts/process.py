import csv
import json
import geojson

fp = 'data/US_Rendition_FOIA.csv'
fpout = 'data/US_Rendition_FOIA.geojson.csv'
jsonout = 'data/US_Rendition_FOIA.geojson.json'

jsondata = []
def convert():
    reader = csv.DictReader(open(fp))
    writer = csv.DictWriter(open(fpout, 'w'), reader.fieldnames + ['geojson'])
    for row in reader:
        def floatify(data):
            if data:
                return float(data)
            else:
                return None
        try:
            coords = [map(floatify, [row['Departure_Lon'], row['Departure_Lat']]),
                map(floatify, [row['Arrival_Lon'], row['Arrival_Lat']])]
        except:
            print row
            break
        p = geojson.LineString(coords)
        row['geojson'] = geojson.dumps(p)
        writer.writerow(row)
        row['geojson'] = json.loads(geojson.dumps(p))
        jsondata.append(row)
    json.dump(jsondata, open(jsonout, 'w'))


import datastore.client

def upload():
    dsurl = 'http://datahub.io/api/data/ac5a28ea-eb52-4b0a-a399-5dcc1becf9d9'
    dsurl = 'http://localhost:9200/ds/rendition-on-record'
    client = datastore.client.DataStoreClient(dsurl)
    client.delete()
    client.upload(jsonout)

# convert()
import logging
logging.basicConfig(level=logging.DEBUG)
upload()

