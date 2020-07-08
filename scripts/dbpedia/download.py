import requests
import csv

language = {
    "query": '''SELECT REPLACE(STR(?uri),"http://dbpedia.org/resource/","") as ?suffix STR(SAMPLE(?label)) AS ?label
{
 ?uri a dbo:Language;
      rdfs:label ?label;
      dbo:iso6391Code [].
 FILTER(LANGMATCHES(LANG(?label),"en"))
}''',
    "endpoint": "https://dbpedia.org/sparql",
}

#  SWO is uploaded to the HITO endpoint, they are (transitive) subclasses, not instances
license = {
    "query": '''PREFIX swo: <http://www.ebi.ac.uk/swo/license/>
SELECT REPLACE(STR(?uri),"http://www.ebi.ac.uk/swo/","") as ?suffix STR(SAMPLE(?label)) AS ?label
FROM <http://www.ebi.ac.uk/swo/swo.owl/1.7>
{
 ?uri rdfs:subClassOf+ swo:SWO_0000002;
      rdfs:label ?label.
 FILTER(LANGMATCHES(LANG(?label),"en"))
}''',
    "endpoint": "https://hitontology.eu/sparql"
}

programmingLanguage = {
    "query": '''SELECT REPLACE(STR(?uri),"http://dbpedia.org/resource/","") as ?suffix STR(SAMPLE(?label)) AS ?label
{
 ?uri a yago:WikicatProgrammingLanguages ;
      rdfs:label ?label.
 FILTER(LANGMATCHES(LANG(?label),"en"))
}''',
    "endpoint": "https://dbpedia.org/sparql"
}

classes = [programmingLanguage]

for clazz in classes:
    parameters = {"query": clazz["query"], "format": "text/comma-separated-values"}
    resp = requests.get(clazz["endpoint"],params=parameters)
    tsv = resp.text
     
