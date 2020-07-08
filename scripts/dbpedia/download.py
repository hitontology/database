import requests
import csv
import os

language = {
    "query": '''SELECT REPLACE(STR(?uri),"http://dbpedia.org/resource/","") as ?suffix STR(SAMPLE(?label)) AS ?label
{
 ?uri a dbo:Language;
      rdfs:label ?label;
      dbo:iso6391Code [].
 FILTER(LANGMATCHES(LANG(?label),"en"))
}''',
    "endpoint": "https://dbpedia.org/sparql",
    "table": "language"
}

#  SWO is uploaded to the HITO endpoint, they are (transitive) subclasses, not instances
license = {
    "query": '''PREFIX swo: <http://www.ebi.ac.uk/swo/>
SELECT REPLACE(STR(?uri),"http://www.ebi.ac.uk/swo/","") as ?suffix STR(SAMPLE(?label)) AS ?label
FROM <http://www.ebi.ac.uk/swo/swo.owl/1.7>
{
 ?uri rdfs:subClassOf+ swo:SWO_0000002;
      rdfs:label ?label.
 FILTER(LANGMATCHES(LANG(?label),"en"))
}''',
    "endpoint": "https://hitontology.eu/sparql",
    "table": "license"
}

programmingLanguage = {
    "query": '''SELECT REPLACE(STR(?uri),"http://dbpedia.org/resource/","") as ?suffix STR(SAMPLE(?label)) AS ?label
{
 ?uri a yago:WikicatProgrammingLanguages ;
      rdfs:label ?label.
 FILTER(LANGMATCHES(LANG(?label),"en"))
}''',
    "endpoint": "https://dbpedia.org/sparql",
    "table": "programmingLanguage"
}

classes = [language,license,programmingLanguage]

for clazz in classes:
    filename=clazz['table']+".sql"
    output=open(filename, "w")
    output.write("DELETE FROM "+clazz['table']+";\n")
    output.write("INSERT INTO "+clazz['table']+"(suffix,label) VALUES"+'\n')
    parameters = {"query": clazz["query"], "format": "text/tab-separated-values"}
    resp = requests.get(clazz["endpoint"],params=parameters)
    readCSV = csv.reader(resp.text.splitlines(), delimiter='\t')
    next(readCSV, None)
    print(resp.text)
    for line in readCSV:
        output.write('(E\''+line[0].replace("'","\\'")+'\',E\''+line[1].replace("'","\\'")+'\'),\n')
#        print(line)
#        pass
#        print('(\''+line[0]+'\',\''+line[1])
     
    output.close()
    #truncate last char of the file and replace it with ;
    with open(filename, 'rb+') as filehandle:
        filehandle.seek(-2, os.SEEK_END)
        filehandle.truncate()
    with open (filename, "a+") as append:
        append.write(';')
