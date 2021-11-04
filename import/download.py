# Download classes from the HITO SPARQL endpoint
# Not using the CSV2RDF tables because some products are not there but included in the base hito.ttl file.
# Those need to be removed from hito.ttl afterwards.

import requests
import csv
import os
import shutil
from classes import classes


def escape(s):
    return "E'" + s.replace("'", "''") + "'"  # escape single quotes, add quotes for SQL


def valueMap(value, isArray):
    if isArray:
        values = filter(None, value.split("|"))  # remove empty strings on empty results
        return (
            "'{"
            + ",".join(map(lambda v: '"' + v.replace("'", "''") + '"', values))
            + "}'"
        )
    if value == "" or value.startswith("Unknown"):
        return "NULL"
    return escape(value)


def insert(values, arrayfields):
    mapped = []
    for i in range(len(values)):
        mapped.append(valueMap(values[i], i in arrayfields))
    s = ",".join(mapped)
    return "(" + s + ")"


DEBUG = os.environ.get("SQL_DEBUG") is not None

SQL_OUTPUT_BASE_DIR_DEFAULT = "/tmp/sql/"
outputBase = os.environ.get("SQL_OUTPUT_BASE_DIR")
if outputBase == None:
    outputBase = SQL_OUTPUT_BASE_DIR_DEFAULT
    print(
        "Environment variable SQL_OUTPUT_BASE_DIR not set, using default value",
        outputBase,
    )
if not outputBase.endswith("/"):
    outputBase += "/"
#if os.path.exists(outputBase):
#    shutil.rmtree(outputBase)
os.makedirs(outputBase, 0o777, True)
allFileName = outputBase+"hito.sql"
if os.path.exists(allFileName):
    print("Target file already exist. Skipping download.")
    exit(0)
allFile = open(allFileName, "w")
with open("base/schema.sql", "r") as schema:
    shutil.copyfileobj(schema, allFile)
with open("base/catalogues.sql", "r") as catalogues:
    shutil.copyfileobj(catalogues, allFile)
for clazz in classes:
    filename = clazz["table"] + ".sql"
    parameters = {"query": clazz["query"], "format": "text/tab-separated-values"}
    resp = requests.get(clazz["endpoint"], params=parameters)
    if resp.status_code != 200:
        print("Error with SPARQL query :\n" + resp.text)
        continue
    readCSV = csv.reader(resp.text.splitlines(), delimiter="\t")
    next(readCSV, None)  # skip CSV header
    rows = list(readCSV)
    if len(rows) == 0:
        print(f"""No entries found for {clazz["table"]}:\n{clazz["query"]}""")
    else:
        print("Downloading class " + clazz["table"])
        content = "\\echo FILL TABLE " + clazz["table"] + "\n"
        content += "DELETE FROM " + clazz["table"] + ";\n"
        content += "INSERT INTO " + clazz["table"] + clazz["fields"] + " VALUES" + "\n"
        content += ",\n".join(
            map(lambda line: insert(line, clazz["arrayfields"]), rows)
        )
        content += content
        content += "ON CONFLICT DO NOTHING;"  # skip duplicates instead of cancelling, only for testing
        if DEBUG:
            folder = outputBase + clazz["folder"]
            if not os.path.exists(folder):
                os.makedirs(folder, 0o777, True)
            with open(folder + "/" + filename, "w") as singleFile:
                singleFile.write(content)
        allFile.write(content)
allFile.close()
