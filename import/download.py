# Download classes from the HITO SPARQL endpoint
# Not using the CSV2RDF tables because some products are not there but included in the base hito.ttl file.
# Those need to be removed from hito.ttl afterwards.

import requests
import csv
import os
import shutil
import rdflib
import oxrdflib
import timeit
from functools import reduce
from classes import classes

start = timeit.default_timer()

PROFILE = os.environ.get("DOWNLOAD_PROFILE") is not None
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
    print("Target file",allFileName,"already exists. Skipping download.")
    exit(0)

def escape(s):
    return "E'" + s.strip().replace("'", "''").replace("\n"," ") + "'"  # escape single quotes, replace newlines with spaces, add quotes for SQL


def valueMap(value, isArray):
    if isArray:
        values = filter(None, value.split("|"))  # remove empty strings on empty results
        values = filter(lambda x: x!="None", values) # remove empty results from RDFLib optional GROUP_CONCAT
        return (
            "'{"
            + ",".join(map(lambda v: '"' + v.replace("'", "''") + '"', values))
            + "}'"
        )
    if value == None or value == "" or value.startswith("Unknown"):
        return "NULL"
    return escape(value)


def insert(values, arrayfields):
    mapped = []
    for i in range(len(values)):
        mapped.append(valueMap(values[i], i in arrayfields))
    s = ",".join(mapped)
    return "(" + s + ")"

# workaround for Oxigraph problem, reported at https://github.com/oxigraph/oxrdflib/issues/10
prefixes = """PREFIX hito: <http://hitontology.eu/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dce: <http://purl.org/dc/elements/1.1/>
"""
def main():
    allFile = open(allFileName, "w")
    with open("base/schema.sql", "r") as schema:
        shutil.copyfileobj(schema, allFile)
    with open("base/catalogues.sql", "r") as catalogues:
        shutil.copyfileobj(catalogues, allFile)
        stats = []
    for clazz in classes:
        filename = clazz["table"] + ".sql"
        rows = []
        datasource = clazz["datasource"]
        match(datasource["type"]):
            case "file":
                if not "graph" in datasource:
                    graph = rdflib.Graph(store="Oxigraph")
                    graph.parse(datasource["value"])
                    graph.namespace_manager.bind('hito', rdflib.URIRef('http://hitontology.eu/ontology/'))
                    graph.namespace_manager.bind('skos', rdflib.namespace.SKOS, override=False)
                    graph.namespace_manager.bind('rdfs', rdflib.namespace.RDFS, override=False)
                    datasource["graph"] = graph
                graph = datasource["graph"]
                try:
                    # https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.query.Result
                    #rows = list(graph.query(clazz["query"]))
                    query = prefixes+clazz["query"]
                    rows = graph.query(query) # workaround for oxigraph problem
                except Exception as e:
                    print("Error with SPARQL query, aborting *******************\n",query,"\n*****************************\n",e)
                    exit(1)

            case "endpoint":
                parameters = {"query": clazz["query"], "format": "text/tab-separated-values"}
                resp = requests.get(datasource["value"], params=parameters)
                if resp.status_code != 200:
                    print("Error with SPARQL query :\n" + resp.text)
                    continue
                readCSV = csv.reader(resp.text.splitlines(), delimiter="\t")
                next(readCSV, None)  # skip CSV header
                rows = list(readCSV)
            case _:
                print("Unknown type \""+datasource["type"]+"\". Aborting")
                exit(1)
            #print(list(rows))
        if len(rows) == 0:
            print(f"""No entries found for {clazz["table"]} with query:\n{clazz["query"]}""")
        else:
            if len(rows) == 1:
                print(f"""Only one entry {(list(rows)[0])} found for {clazz["table"]} with query:\n{clazz["query"]}""")
            #print("Downloaded class " + clazz["table"],"["+str(len(rows))+"]")
            stats.append((clazz["table"],len(rows)))
            content = "\\echo Filling table " + clazz["table"] + " with " + str(len(rows)) + " rows...\n"
            content += "DELETE FROM " + clazz["table"] + ";\n"
            content += "INSERT INTO " + clazz["table"] + clazz["fields"] + " VALUES\n"
            content += ",\n".join(
                map(lambda line: insert(line, clazz["arrayfields"]), rows)
            ) + "\n"
            content += "ON CONFLICT DO NOTHING;\n"  # skip duplicates instead of cancelling, only for testing
            if DEBUG:
                folder = outputBase + clazz["folder"]
                if not os.path.exists(folder):
                    os.makedirs(folder, 0o777, True)
                with open(folder + "/" + filename, "w") as singleFile:
                    singleFile.write(content)
            allFile.write(content)
    statprint = lambda s: s[0]+" ["+str(s[1])+"]"
    stop = timeit.default_timer()
    print("Successfully downloaded",reduce(lambda a,b: a+" "+b,map(statprint, stats)),"in",int(stop-start),"seconds.")
    allFile.close()

if __name__ == "__main__":
    main()
