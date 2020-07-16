import requests
import csv
import os

standard = {
    "query": '''SELECT REPLACE(STR(?uri),"http://hitontology.eu/ontology/","") as ?suffix
        STR(SAMPLE(?label)) AS ?label
        STR(SAMPLE(?comment)) AS ?comment
        GROUP_CONCAT(?source;separator="|") AS ?sources
 {
  ?uri a hito:Interoperability;
          rdfs:label ?label;
          rdfs:comment ?z;
          <http://purl.org/dc/terms/source> ?source.
}''',
    "endpoint": "https://hitontology.eu/sparql",
    "table": "interoperabilityStandard",
    "fields": "(suffix, label, comment, sourceuris)"
}

language = {
    "query": '''SELECT REPLACE(STR(?uri),"http://dbpedia.org/resource/","") as ?suffix STR(SAMPLE(?label)) AS ?label
{
 ?uri a dbo:Language;
      rdfs:label ?label;
      dbo:iso6391Code [].
 FILTER(LANGMATCHES(LANG(?label),"en"))
}''',
    "endpoint": "https://dbpedia.org/sparql",
    "table": "language",
    "fields": "(suffix, label)"
}

#  SWO is uploaded to the HITO endpoint, they are (transitive) subclasses, not instances
license = {
    "query": '''PREFIX swo: <http://www.ebi.ac.uk/swo/>
SELECT REPLACE(STR(?uri),"http://www.ebi.ac.uk/swo/","") as ?suffix STR(SAMPLE(?label)) AS ?label
#FROM <http://www.ebi.ac.uk/swo/swo.owl/1.7>
{
 ?uri rdfs:subClassOf+ swo:SWO_0000002;
      rdfs:label ?label.
 FILTER(LANGMATCHES(LANG(?label),"en"))
}''',
    "endpoint": "https://hitontology.eu/sparql",
    "table": "license",
    "fields": "(suffix, label)"
}

programmingLanguage = {
    "query": '''SELECT REPLACE(STR(?uri),"http://dbpedia.org/resource/","") as ?suffix STR(SAMPLE(?label)) AS ?label
{
 ?uri a yago:WikicatProgrammingLanguages ;
      rdfs:label ?label.
 FILTER(LANGMATCHES(LANG(?label),"en"))
}''',
    "endpoint": "https://dbpedia.org/sparql",
    "table": "programmingLanguage",
    "fields": "(suffix, label)"
}


def valueMap(value,isArray):
    if(isArray):
        return "'{" + ",".join(map(lambda v: '"'+v+'"', value.split("|")))  + "}'"
    if(value==''):
        return 'NULL'
    return "E'"+value.replace("'","\\'")+"'" # escape single quotes, add quotes for SQL

def insert(values):
    mapped = []
    for i in range(len(values)):
        mapped.append(valueMap(values[i],i==3)) # there can be more than one source, it is at position 3 counting from 0 
    s = ",".join(mapped) 
    return "("+s+")"

classes = [standard,language,license,programmingLanguage]

for clazz in classes:
    filename=clazz['table']+".sql"
    output=open("attribute/"+filename, "w")
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
