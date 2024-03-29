import os

suffix = lambda s: f'REPLACE(STR({s}),".*/","")'
concat = lambda s: f'GROUP_CONCAT(DISTINCT({s});separator="|")'

datasources = {
    "HITO": {
        "name": "HITO_FILE",
        "type": "file",
        "default": "../../ontology/dist/hito.ttl",
    },
    "HITO_ENDPOINT": {
        "name": "HITO_SPARQL_ENDPOINT",
        "type": "endpoint",
        "default": "https://hitontology.eu/sparql",
    },
    "DBPEDIA_ENDPOINT": {
        "name": "DBPEDIA_SPARQL_ENDPOINT",
        "type": "endpoint",
        "default": "https://dbpedia.org/sparql",
    },
    "DBPEDIA": {
        "name": "DBPEDIA_FILE",
        "type": "file",
        "default": "../../ontology/dist/dbpedia.ttl",
    },
    "SWO": {
        "name": "SWO_FILE",
        "type": "file",
        "default": "../../ontology/dist/swo.ttl",
    },
}

for key, datasource in datasources.items():
    datasource["value"] = os.environ.get(datasource["name"])
    if datasource["value"] == None:
        print(
            "Environment variable",
            datasource["name"],
            "not set, using default value",
            datasource["default"],
        )
        datasource["value"] = datasource["default"]

standard = {
        "query": f"""
   SELECT
        (REPLACE(STR(?uri),"http://hitontology.eu/ontology/","") AS ?suffix)
        (STR(SAMPLE(?l)) AS ?label)
        (STR(SAMPLE(?z)) AS ?comment)
        ({concat("?source")} AS ?sources)
{{
  ?uri a hito:Interoperability;
          rdfs:label ?l.

  OPTIONAL {{?uri <http://purl.org/dc/terms/source> ?source.}}
  OPTIONAL {{?uri rdfs:comment ?z.}}
}}
GROUP BY ?uri
ORDER BY ASC(?uri)""",
    "folder": "attribute",
    "datasource": datasources["HITO"],
    "table": "interoperabilitystandard",
    "fields": "(suffix, label, comment, sourceuris)",
    "arrayfields": [3],
}

language = {
    "query": """SELECT (REPLACE(STR(?uri),"http://dbpedia.org/resource/","") AS ?suffix) (STR(SAMPLE(?l)) AS ?label)
{
 ?uri a <http://dbpedia.org/ontology/Language>;
      rdfs:label ?l.
 FILTER(LANGMATCHES(LANG(?l),"en")||LANGMATCHES(LANG(?l),""))
}
GROUP BY ?uri
ORDER BY ASC(?uri)""",
    "folder": "attribute",
    "datasource": datasources["DBPEDIA"],
    "table": "language",
    "fields": "(suffix, label)",
    "arrayfields": [],
}

#  SWO is uploaded to the HITO endpoint, they are (transitive) subclasses, not instances
# Model as hito:License as RDFLib seems to have problemy with property paths.
# Langmatches filter seems to not work properly with RDFLib, comment it out.
license = {
    "query": """PREFIX swo: <http://www.ebi.ac.uk/swo/>
SELECT
(REPLACE(STR(?uri),"http://www.ebi.ac.uk/swo/license/","") AS ?suffix)
(STR(SAMPLE(?l)) AS ?label)
#FROM <http://www.ebi.ac.uk/swo/swo.owl/1.7>
{
 ?uri a hito:License;
 #?uri rdfs:subClassOf+ swo:SWO_0000002;
      rdfs:label ?l.
 #FILTER((LANGMATCHES(LANG(?l),"en")) || (LANGMATCHES(LANG(?l),"")))
}
GROUP BY ?uri
ORDER BY ASC(?uri)
""",
    "folder": "attribute",
    "datasource": datasources["SWO"],
    "table": "license",
    "fields": "(suffix,label)",
    "arrayfields": [],
}

programmingLanguage = {
    "query": """SELECT (REPLACE(STR(?uri),"http://dbpedia.org/resource/","") AS ?suffix) (STR(SAMPLE(?l)) AS ?label)
{
# ?uri a yago:WikicatProgrammingLanguages ;
 ?uri a <http://dbpedia.org/ontology/ProgrammingLanguage> ;
      rdfs:label ?l.
 FILTER(LANGMATCHES(LANG(?l),"en")||LANGMATCHES(LANG(?l),""))
}
GROUP BY ?uri
ORDER BY ASC(?uri)""",
    "folder": "attribute",
    "datasource": datasources["DBPEDIA"],
    "table": "programminglanguage",
    "fields": "(suffix, label)",
    "arrayfields": [],
}

programmingLibrary = {
    "query": """SELECT (REPLACE(STR(?uri),"http://hitontology.eu/ontology/","") AS ?suffix) (STR(SAMPLE(?l)) AS ?label)
{
 ?uri a hito:ProgrammingLibrary ;
      rdfs:label ?l.
 FILTER(LANGMATCHES(LANG(?l),"en")||LANGMATCHES(LANG(?l),""))
}
GROUP BY ?uri
ORDER BY ASC(?uri)""",
    "folder": "attribute",
    "datasource": datasources["HITO"],
    "table": "programminglibrary",
    "fields": "(suffix, label)",
    "arrayfields": [],
}

operatingSystem = {
    "query": """SELECT (REPLACE(STR(?uri),"http://dbpedia.org/resource/","") AS ?suffix) (STR(SAMPLE(?l)) AS ?label)
{
 ?uri a hito:OperatingSystem ;
      rdfs:label ?l.
 FILTER(LANGMATCHES(LANG(?l),"en")||LANGMATCHES(LANG(?l),""))
}
GROUP BY ?uri
ORDER BY ASC(?suffix)""",
    "folder": "attribute",
    "datasource": datasources["DBPEDIA"],
    "table": "operatingsystem",
    "fields": "(suffix, label)",
    "arrayfields": [],
}

softwareProduct = {
    "query": f"""SELECT
({suffix("?uri")} AS ?suffix)
(SAMPLE(STR(?l)) AS ?label)
(STR(SAMPLE(?cmt)) AS ?comment)
(SAMPLE(?repository) AS ?coderepository)
(SAMPLE(?homepage) AS ?homepage)
{{
 ?uri a hito:SoftwareProduct;
      rdfs:label ?l.
 
 OPTIONAL {{?uri rdfs:comment ?cmt.}}
 OPTIONAL {{?uri hito:repository ?repository.}}
 OPTIONAL {{?uri hito:homepage ?homepage.}}

 FILTER(LANGMATCHES(LANG(?l),"en")||LANGMATCHES(LANG(?l),""))
}}
GROUP BY ?uri
ORDER BY ASC(?uri)""",
    "folder": "swp",
    "datasource": datasources["HITO"],
    "table": "softwareproduct",
    "fields": "(suffix, label, comment, coderepository, homepage)",
    "arrayfields": [5, 6],
}

citation = {
    "query": f"""SELECT
(REPLACE(STR(?citation),".*/","") AS ?suffix)
(REPLACE(STR(?uri),".*/","") AS ?swp_suffix)
(STR(SAMPLE(?l)) AS ?label)
(STR(SAMPLE(?cmt)) AS ?comment)
(REPLACE(STRAFTER(STR(?t),"ontology/"),"Citation","") AS ?type)
{{
 ?uri a  hito:SoftwareProduct;
     ?p ?citation.
     ?p rdfs:subPropertyOf hito:citation.
  ?citation a ?t.
  BIND(REPLACE(STR(?p),".*/","") AS ?p_suffix).

 ?citation rdfs:label ?l.
 OPTIONAL {{?citation rdfs:comment ?cmt.}}
}}
GROUP BY ?citation ?uri ?p_suffix ?t
ORDER BY ASC(?swp_suffix) ASC(?suffix)""",
    "folder": "swp",
    "datasource": datasources["HITO"],
    "table": "citation",
    "fields": "(suffix,swp_suffix, label,comment,type)",
    "arrayfields": [],
}

classified = {
    "query": f"""
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dce: <http://purl.org/dc/elements/1.1/>
SELECT
?suffix
(REPLACE(STR(?catalogue),".*/","") AS ?catalogue_suffix)
(STR(SAMPLE(?n)) AS ?n)
(STR(SAMPLE(?l)) AS ?label)
(STR(SAMPLE(?cmt)) AS ?comment)
({concat("STR(?synonym)")} AS ?synonyms)
({concat("STR(?dct_source)")} AS ?dct_sources)
({concat("STR(?dce_source)")} AS ?dce_sources)
{{
 ?classified ?p ?catalogue;
             rdfs:label ?l.
 #FILTER(?classified=<http://hitontology.eu/ontology/BbCardiovascularInformationSystem>) 
 
 OPTIONAL {{?classified rdfs:comment ?cmt.}}
 OPTIONAL {{?classified skos:altLabel ?synonym.}}
 OPTIONAL {{?classified hito:memberNr ?n.}}
 OPTIONAL {{?classified dct:source ?dct_source.}}
 OPTIONAL {{?classified dce:source ?dce_source.}}
 ?p rdfs:subPropertyOf hito:catalogue.

 BIND(REPLACE(STR(?classified),".*/","") AS ?suffix)
 FILTER(!STRSTARTS(STR(?suffix),"Unknown")) # We treat UnknownX instances as NULL in DB
}}
GROUP BY ?suffix ?catalogue
ORDER BY ASC(?suffix)""",
    "folder": "catalogue",
    "datasource": datasources["HITO"],
    "table": "classified",
    "fields": "(suffix,catalogue_suffix,n,label,comment,synonyms,dct_source,dce_sources)",
    "arrayfields": [5, 6, 7],
}
# workaround to exclude study citations

citation_has_classified = {
    "query": f"""
SELECT
({suffix("?citation")} AS ?citation_suffix)
({suffix("?classified")} AS ?classified_suffix)
{{
    ?citation ?p ?classified.
    ?classified a [rdfs:subClassOf hito:Classified].
    ?p rdfs:subPropertyOf hito:classified.
    
    ?swp a hito:SoftwareProduct; ?q ?citation.
}}
GROUP BY ?citation ?classified
HAVING (COUNT(?swp)>=1)
ORDER BY ASC(?citation_suffix) ASC(?classified_suffix)
""",
    "folder": "relation",
    "datasource": datasources["HITO"],
    "table": "citation_has_classified",
    "fields": "(citation_suffix,classified_suffix)",
    "arrayfields": [],
}

classifiedComponent = {
    "query": f"""
SELECT
({suffix("?parent")} AS ?parent_suffix)
({suffix("?child")} AS ?child_suffix)
{{
 ?child ?p ?parent.
 ?p rdfs:subPropertyOf hito:subClassifiedOf.
}}
ORDER BY ASC(?parent_suffix) ASC(?child_suffix)""",
    "folder": "relation",
    "datasource": datasources["HITO"],
    "table": "classified_has_child",
    "fields": "(parent_suffix,child_suffix)",
    "arrayfields": [],
}

featureSupportsFunction = {
    "query": f"""
SELECT
({suffix("?feature")} AS ?feature_suffix)
({suffix("?function")} AS ?function_suffix)
{{
 ?feature hito:supportsFunction ?function.
}}
ORDER BY ASC(?feature_suffix) ASC(?function_suffix)""",
    "folder": "relation",
    "datasource": datasources["HITO"],
    "table": "feature_supports_function",
    "fields": "(feature_suffix,function_suffix)",
    "arrayfields": [],
}

# Properties candidates for the query were determined via:
# SELECT DISTINCT ?p {?s a hito:SoftwareProduct; ?p ?o.}
# Of those we only use properties that don't have their own database table in the first query for simpler mapping and to reduce OPTIONAL statements.

relationData = [
    {
        "p": "softwareProductComponent",
        "table": "swp_has_child",
        "fieldList": ["parent_suffix", "child_suffix"],
    },
    {
        "p": "interoperability",
        "table": "swp_has_interoperabilitystandard",
        "fieldList": ["swp_suffix", "io_suffix"],
    },
    {
        "p": "language",
        "table": "swp_has_language",
        "fieldList": ["swp_suffix", "lang_suffix"],
    },
    {
        "p": "license",
        "table": "swp_has_license",
        "fieldList": ["swp_suffix", "license_suffix"],
    },
    {
        "p": "operatingSystem",
        "table": "swp_has_operatingsystem",
        "fieldList": ["swp_suffix", "os_suffix"],
    },
    {
        "p": "programmingLanguage",
        "table": "swp_has_programminglanguage",
        "fieldList": ["swp_suffix", "plang_suffix"],
    },
    {
        "p": "programmingLibrary",
        "table": "swp_has_programminglibrary",
        "fieldList": ["swp_suffix", "lib_suffix"],
    },
    {
        "p": "client",
        "table": "swp_has_client",
        "fieldList": ["swp_suffix", "client_suffix"],
    },
    {
        "p": "databaseSystem",
        "table": "swp_has_databasesystem",
        "fieldList": ["swp_suffix", "db_suffix"],
    },
]

relations = map(
    lambda d: {
        "query": f"""SELECT
({suffix("?uri")} as ?swp_suffix)
({suffix("?x")} as ?{d["fieldList"][1]})
{{
 ?uri a hito:SoftwareProduct; hito:{d["p"]} ?x.
}} ORDER BY ASC(?swp_suffix) ASC(?{d["fieldList"][1]})""",
        "folder": "relation",
        "datasource": datasources["HITO"],
        "type": "datasource",
        "table": d["table"],
        "fields": f"({d['fieldList'][0]},{d['fieldList'][1]})",
        "arrayfields": [],
    },
    relationData,
)
classes = [
    standard,
    language,
    license,
    programmingLanguage,
    programmingLibrary,
    operatingSystem,
    softwareProduct,
    classified,
    classifiedComponent,
    citation,
    citation_has_classified,
    featureSupportsFunction,
] + list(relations)

