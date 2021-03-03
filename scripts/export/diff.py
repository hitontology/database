# Download classes from the HITO SPARQL endpoint
# Not using the CSV2RDF tables because some products are not there but included in the base hito.ttl file.
# Those need to be removed from hito.ttl afterwards.

import requests
import csv
import os
import shutil
import re

ENDPOINT = "https://hitontology.eu/sparql/"
CLASSES = ["SoftwareProduct"]

def query(clazz):
    return """CONSTRUCT {?s ?p ?o.}
    {
     ?s a hito:""" + clazz + """.
     ?s ?p ?o.
    }"""

outputBase = "tmp/"
if os.path.exists(outputBase):
    shutil.rmtree(outputBase)
for clazz in CLASSES:
    q = query(clazz)
    parameters = {"query": q, "format": "text/plain"}
    resp = requests.get(ENDPOINT,params=parameters)
    if(resp.status_code!=200):
        print("Error with SPARQL query :\n"+resp.text)
    text = resp.text
    # todo: normalize whitespace to one space
    print(text)

