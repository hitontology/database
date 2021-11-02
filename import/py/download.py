# Download classes from the HITO SPARQL endpoint
# Not using the CSV2RDF tables because some products are not there but included in the base hito.ttl file.
# Those need to be removed from hito.ttl afterwards.

import requests
import csv
import os
import shutil
from classes import classes

def escape(s):
    return "E'"+s.replace("'","''")+"'" # escape single quotes, add quotes for SQL

def valueMap(value,isArray):
    if(isArray):
        values = filter(None,value.split("|")) # remove empty strings on empty results
        return "'{" + ",".join(map(lambda v: '"'+v.replace("'","''")+'"', values))  + "}'"
    if(value=='' or value.startswith('Unknown')):
        return 'NULL'
    return escape(value)

def insert(values,arrayfields):
    mapped = []
    for i in range(len(values)):
        mapped.append(valueMap(values[i],i in arrayfields))
    s = ",".join(mapped) 
    return "("+s+")"

SQL_OUTPUT_BASE_DIR_DEFAULT = "/tmp/sql/"
outputBase = os.environ.get("SQL_OUTPUT_BASE_DIR")
if(outputBase==None):
    outputBase = SQL_OUTPUT_BASE_DIR_DEFAULT
    print("Environment variable SQL_OUTPUT_BASE_DIR not set, using default value",outputBase)
if not outputBase.endswith("/"):
    outputBase+="/"
if os.path.exists(outputBase):
    shutil.rmtree(outputBase)
for clazz in classes:
    filename=clazz['table']+".sql"
    parameters = {"query": clazz["query"], "format": "text/tab-separated-values"}
    resp = requests.get(clazz["endpoint"],params=parameters)
    if(resp.status_code!=200):
        print("Error with SPARQL query :\n"+resp.text)
        continue
    readCSV = csv.reader(resp.text.splitlines(), delimiter='\t')
    next(readCSV, None) # skip CSV header
    rows = list(readCSV)
    if len(rows)==0:
        print(f"""No entries found for {clazz["table"]}:\n{clazz["query"]}""")
    else:
        folder= outputBase+clazz["folder"]
        if not os.path.exists(folder):
            os.makedirs(folder,0o777,True)
        output=open(folder+"/"+filename, "w")
        print("Downloading class "+clazz["table"])
        output.write("\\echo FILL TABLE "+clazz['table']+"\n")
        output.write("DELETE FROM "+clazz['table']+";\n")
        output.write("INSERT INTO "+clazz['table']+clazz['fields']+" VALUES"+'\n')
        content = ",\n".join(map(lambda line: insert(line,clazz["arrayfields"]), rows))
        output.write(content)
        output.write("ON CONFLICT DO NOTHING") # skip duplicates instead of cancelling, only for testing
        output.write(";")
        output.close()
