suffix = lambda s: f'REPLACE(STR({s}),".*/","")'
concat = lambda s: f'GROUP_CONCAT(DISTINCT({s});separator="|")';

standard = {
    "query": f'''SELECT REPLACE(STR(?uri),"http://hitontology.eu/ontology/","") as ?suffix
        STR(SAMPLE(?label)) AS ?label
        STR(SAMPLE(?comment)) AS ?comment
        {concat("?source")} AS ?sources
{{
  ?uri a hito:Interoperability;
          rdfs:label ?label.

  OPTIONAL {{?uri <http://purl.org/dc/terms/source> ?source.}}
  OPTIONAL {{?uri rdfs:comment ?z.}}
}}''',
    "folder": "attribute",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "InteroperabilityStandard",
    "fields": "(suffix, label, comment, sourceuris)",
    "arrayfields": [3]
}

language = {
    "query": '''SELECT REPLACE(STR(?uri),"http://dbpedia.org/resource/","") as ?suffix STR(SAMPLE(?label)) AS ?label
{
 ?uri a dbo:Language;
      rdfs:label ?label;
      dbo:iso6391Code [].
 FILTER(LANGMATCHES(LANG(?label),"en")||LANGMATCHES(LANG(?label),""))
}''',
    "folder": "attribute",
    "endpoint": "https://dbpedia.org/sparql",
    "table": "Language",
    "fields": "(suffix, label)",
    "arrayfields": []
}

#  SWO is uploaded to the HITO endpoint, they are (transitive) subclasses, not instances
license = {
    "query": '''PREFIX swo: <http://www.ebi.ac.uk/swo/>
SELECT REPLACE(STR(?uri),"http://www.ebi.ac.uk/swo/license/","") as ?suffix STR(SAMPLE(?label)) AS ?label
#FROM <http://www.ebi.ac.uk/swo/swo.owl/1.7>
{
 ?uri rdfs:subClassOf+ swo:SWO_0000002;
      rdfs:label ?label.
 FILTER(LANGMATCHES(LANG(?label),"en")||LANGMATCHES(LANG(?label),""))
}''',
    "folder": "attribute",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "License",
    "fields": "(suffix, label)",
    "arrayfields": []
}

programmingLanguage = {
    "query": '''SELECT REPLACE(STR(?uri),"http://dbpedia.org/resource/","") as ?suffix STR(SAMPLE(?label)) AS ?label
{
 ?uri a yago:WikicatProgrammingLanguages ;
      rdfs:label ?label.
 FILTER(LANGMATCHES(LANG(?label),"en")||LANGMATCHES(LANG(?label),""))
}''',
    "folder": "attribute",
    "endpoint": "https://dbpedia.org/sparql",
    "table": "ProgrammingLanguage",
    "fields": "(suffix, label)",
    "arrayfields": []
}

operatingSystem = {
    "query": '''SELECT REPLACE(STR(?uri),"http://dbpedia.org/resource/","") as ?suffix STR(SAMPLE(?label)) AS ?label
{
 ?uri a hito:OperatingSystem ;
      rdfs:label ?label.
 FILTER(LANGMATCHES(LANG(?label),"en")||LANGMATCHES(LANG(?label),""))
}''',
    "folder": "attribute",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "OperatingSystem",
    "fields": "(suffix, label)",
    "arrayfields": []
}

softwareProduct = {
    "query": f'''SELECT
{suffix("?uri")} as ?suffix
SAMPLE(STR(?label)) AS ?label
STR(SAMPLE(?comment)) AS ?comment
SAMPLE(?repository) AS ?coderepository
SAMPLE(?homepage) AS ?homepage
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
    "folder": "swp",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "SoftwareProduct",
    "fields": "(suffix, label, comment, coderepository, homepage, clients, databaseSystems)",
    "arrayfields": [5,6]
}
#print(softwareProduct["query"])

citation = {
    "query": f'''SELECT
REPLACE(STR(?uri),".*/","") as ?swp_suffix
REPLACE(STR(?citation),".*/","") as ?suffix
REPLACE(STR(?classified),".*/","") as ?classified_suffix
STR(SAMPLE(?label)) AS ?label
{{
 ?uri a  hito:SoftwareProduct;
       ?p ?citation.
        ?p rdfs:subPropertyOf hito:citation.

         ?citation ?q ?classified;
                    rdfs:label ?label.
                     ?q rdfs:subPropertyOf hito:classified.
}}''',
    "folder": "relation",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "Citation",
    "fields": "(swp_suffix, suffix, classified_suffix, label)",
    "arrayfields": []
}

# Properties candidates for the query were determined via:
# SELECT DISTINCT ?p {?s a hito:SoftwareProduct; ?p ?o.}
# Of those we only use properties that don't have their own database table in the first query for simpler mapping and to reduce OPTIONAL statements.

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
    "folder": "relation",
    "endpoint": "https://hitontology.eu/sparql",
    "table": d['table'],
    "fields": f"({d['fieldList'][0]},{d['fieldList'][1]})",
    "arrayfields": []
}
, relationData)

classes = [standard,language,license,programmingLanguage,operatingSystem,softwareProduct,citation] + list(relations)

