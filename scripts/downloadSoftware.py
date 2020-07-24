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

suffix = lambda s: f'REPLACE(STR({s}),".*/","")'
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

 FILTER(LANGMATCHES(LANG(?label),"en")||LANGMATCHES(LANG(?label),""))
}}''',
    "endpoint": "https://hitontology.eu/sparql",
    "table": "SoftwareProduct",
    "fields": "(suffix, label, comment, coderepository, homepage, clients, databaseSystems)"
}
#print(softwareProduct["query"])

citation = {
    "query": f'''SELECT
REPLACE(STR(?uri),".*/","") as ?swp_suffix
REPLACE(STR(?citation),".*/","") as ?suffix
REPLACE(STR(?classified),".*/","") as ?classified_suffix
GROUP_CONCAT(DISTINCT(STR(?label));separator="|") AS ?label
{{
 ?uri a  hito:SoftwareProduct;
       ?p ?citation.
        ?p rdfs:subPropertyOf hito:citation.

         ?citation ?q ?classified;
                    rdfs:label ?label.
                     ?q rdfs:subPropertyOf hito:classified.
}}''',
    "endpoint": "https://hitontology.eu/sparql",
    "table": "Citation",
    "fields": "(swp_suffix, suffix, classified_suffix, label)"
}
#print(citation["query"])

relationData = [
{"p": "softwareProductComponent", "table": "swp_has_child", "fieldList": ["parent_suffix", "child_suffix"]},
{"p": "interoperability", "table": "swp_has_interoperabilitystandard", "fieldList": ["swp_suffix", "io_suffix"]},
{"p": "language", "table": "swp_has_language", "fieldList": ["swp_suffix", "lang_suffix"]},
{"p": "license", "table": "swp_has_license", "fieldList": ["swp_suffix", "license_suffix"]},
{"p": "operatingSystem", "table": "swp_has_operatingsystem", "fieldList": ["swp_suffix", "os_suffix"]},
{"p": "programmingLanguage", "table": "swp_has_programminglanguage", "fieldList": ["swp_suffix", "plang_suffix"]},
{"p": "programmingLibrary", "table": "swp_has_programminglibrary", "fieldList": ["swp_suffix", "lib_suffix"]}
]

relations = map(lambda d: {
    "query": f'''SELECT
{suffix("?uri")} as ?swp_suffix
{suffix("?x")} as ?{d["fieldList"][1]}
{{
 ?uri a hito:SoftwareProduct; hito:{d["p"]} ?x.
}}''',
    "endpoint": "https://hitontology.eu/sparql",
    "table": d['table'],
    "fields": f"({d['fieldList'][0]},{d['fieldList'][1]})"
}
, relationData)

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

classes = [softwareProduct,citation] + list(relations)

for clazz in classes:
    filename=clazz['table']+".sql"
    parameters = {"query": clazz["query"], "format": "text/tab-separated-values"}
    resp = requests.get(clazz["endpoint"],params=parameters)
    if(resp.status_code!=200):
        print("Error with SPARQL query :\n"+resp.text)
        continue
    readCSV = csv.reader(resp.text.splitlines(), delimiter='\t')
    next(readCSV, None) # skip CSV header
    content = ",\n".join(map(lambda line: insert(line), readCSV))
    if(content == ""):
        print(f"""No entries found for {clazz["table"]}""") #:\n{clazz["query"]}""")
    else:
        output=open(outputBase+"/"+filename, "w")
        output.write(f"\echo Importing {clazz['table']} from {clazz['endpoint']} \n")
        output.write("DELETE FROM "+clazz['table']+";\n")
        output.write("INSERT INTO "+clazz['table']+clazz['fields']+" VALUES"+'\n')
        output.write(content)
        output.write(";")
        output.close()
