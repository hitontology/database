# Download all software products from the HITO SPARQL endpoint
# Not using the CSV2RDF tables because some products are not there but included in the base hito.ttl file.
# Those need to be removed from hito.ttl afterwards.

import requests
import csv
import os

outputBase = "swp"
os.makedirs(outputBase,0o777,True)

# Properties candidates for the query were determined via:
# SELECT DISTINCT ?p {?s a hito:SoftwareProduct; ?p ?o.}
# Of those we only use properties that don't have their own database table in the first query for simpler mapping and to reduce OPTIONAL statements.

suffix = lambda s: f'REPLACE(STR({s}),"http://hitontology.eu/ontology/","")'
concat = lambda s: f'GROUP_CONCAT(DISTINCT({s});separator="|")';

softwareProduct = {
    "query": f'''SELECT
{suffix("?uri")} as ?suffix
SAMPLE(STR(?label)) AS ?label
STR(SAMPLE(?comment)) AS ?comment
{concat("?repository")} AS ?coderepository
{concat("?homepage")} AS ?homepage
{concat(suffix("?client"))} AS ?clients
{concat(suffix("?databaseSystem"))} as ?dbs
{{
 ?uri a hito:SoftwareProduct;
      rdfs:label ?label.
 
 OPTIONAL {{?uri rdfs:comment ?comment.}}
 OPTIONAL {{?uri hito:repository ?repository.}}
 OPTIONAL {{?uri hito:homepage ?homepage.}}
 OPTIONAL {{?uri hito:client ?client.}}
 OPTIONAL {{?uri hito:databaseSystem ?databaseSystem.}}

 FILTER(LANGMATCHES(LANG(?label),"en"))
}}''',
    "endpoint": "https://hitontology.eu/sparql",
    "table": "SoftwareProduct",
    "fields": "(suffix, label, comment, coderepository, homepage, clients, databaseSystems)"
}

def valueMap(value,isArray):
    if(isArray):
        values = filter(None,value.split("|")) # remove empty strings on empty results
        return "'{" + ",".join(map(lambda v: '"'+v+'"', values ))  + "}'"
    if(value==''):
        return 'NULL'
    return "E'"+value.replace("'","\\'")+"'" # escape single quotes, add quotes for SQL

def insert(values):
    mapped = []
    for i in range(len(values)):
        mapped.append(valueMap(values[i],i>4)) # there can be more than one source, it is at position 3 counting from 0 
    s = ",".join(mapped) 
    return "("+s+")"

classes = [softwareProduct]

for clazz in classes:
    filename=clazz['table']+".sql"
    output=open(outputBase+"/"+filename, "w")
    output.write(f"\echo Importing {clazz['table']} from {clazz['endpoint']} \n")
    output.write("DELETE FROM "+clazz['table']+";\n")
    output.write("INSERT INTO "+clazz['table']+clazz['fields']+" VALUES"+'\n')
    parameters = {"query": clazz["query"], "format": "text/tab-separated-values"}
    resp = requests.get(clazz["endpoint"],params=parameters)
    readCSV = csv.reader(resp.text.splitlines(), delimiter='\t')
    next(readCSV, None) # skip CSV header
    content = ",\n".join(map(lambda line: insert(line), readCSV))
    output.write(content)
    output.write(";")
    output.close()
