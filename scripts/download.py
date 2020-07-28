# Download classes from the HITO SPARQL endpoint
# Not using the CSV2RDF tables because some products are not there but included in the base hito.ttl file.
# Those need to be removed from hito.ttl afterwards.

import requests
import csv
import os
from classes import classes

def valueMap(value,isArray):
    if(isArray):
        values = filter(None,value.split("|")) # remove empty strings on empty results
        return "'{" + ",".join(map(lambda v: '"'+v+'"', values))  + "}'"
    if(value==''):
        return 'NULL'
    return "E'"+value.replace("'","\\'")+"'" # escape single quotes, add quotes for SQL

def insert(values,arrayfields):
    mapped = []
    for i in range(len(values)):
        mapped.append(valueMap(values[i],i in arrayfields))
    s = ",".join(mapped) 
    return "("+s+")"

for clazz in classes:
    print("Downloading "+clazz["table"])
    filename=clazz['table']+".sql"
    parameters = {"query": clazz["query"], "format": "text/tab-separated-values"}
    resp = requests.get(clazz["endpoint"],params=parameters)
    if(resp.status_code!=200):
        print("Error with SPARQL query :\n"+resp.text)
        continue
    readCSV = csv.reader(resp.text.splitlines(), delimiter='\t')
    next(readCSV, None) # skip CSV header
    content = ",\n".join(map(lambda line: insert(line,clazz["arrayfields"]), readCSV))
    if(content == ""):
        print(f"""No entries found for {clazz["table"]}""") #:\n{clazz["query"]}""")
    else:
        outputBase = clazz["folder"]
        os.makedirs(outputBase,0o777,True)
        output=open(outputBase+"/"+filename, "w")
        output.write(f"\echo Importing {clazz['table']} from {clazz['endpoint']} \n")
        output.write("DELETE FROM "+clazz['table']+";\n")
        output.write("INSERT INTO "+clazz['table']+clazz['fields']+" VALUES"+'\n')
        output.write(content)
        output.write("ON CONFLICT DO NOTHING") # skip duplicates instead of cancelling, only for testing
        output.write(";")
        output.close()
