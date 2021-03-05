# Download classes from the HITO SPARQL endpoint
# Not using the CSV2RDF tables because some products are not there but included in the base hito.ttl file.
# Those need to be removed from hito.ttl afterwards.

import requests
import csv
import os
import shutil
import re

ENDPOINT = "https://hitontology.eu/sparql/"
CLASSES = ["[rdfs:subClassOf hito:Citation]"]

def query(clazz):
    return """CONSTRUCT {?s ?p ?o.}
    {
     ?x a """ + clazz + """.
     ?s ?p ?o.
     FILTER(?s=?x OR ?o=?x)
    }"""

QUERIES = [
    """CONSTRUCT {?s ?p ?o.}
    {
     ?x a [rdfs:subClassOf hito:Citation].
     [a hito:SoftwareProduct] ?y ?x. # related to a software product, not a study citation
     ?s ?p ?o.
     FILTER(?s=?x OR ?o=?x)
    }"""
    ]

outputBase = "tmp/"
if os.path.exists(outputBase):
    shutil.rmtree(outputBase)
for q in QUERIES: 
    #q = query(clazz)
    parameters = {"query": q, "format": "text/plain"}
    resp = requests.get(ENDPOINT,params=parameters)
    if(resp.status_code!=200):
        print("Error with SPARQL query :\n"+resp.text)
    text = resp.text
    text = re.sub(r'[ \t]+',' ',text)
    text = "\n".join(sorted(text.split("\n")))
    # todo: normalize whitespace to one space
    print(text)

