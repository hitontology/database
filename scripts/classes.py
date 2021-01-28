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
    "table": "interoperabilitystandard",
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
    "table": "language",
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
    "table": "license",
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
    "table": "programminglanguage",
    "fields": "(suffix, label)",
    "arrayfields": []
}

programmingLibrary = {
    "query": '''SELECT REPLACE(STR(?uri),"http://hitontology.eu/ontology/","") as ?suffix STR(SAMPLE(?label)) AS ?label
{
 ?uri a hito:ProgrammingLibrary ;
      rdfs:label ?label.
 FILTER(LANGMATCHES(LANG(?label),"en")||LANGMATCHES(LANG(?label),""))
}''',
    "folder": "attribute",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "programminglibrary",
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
    "table": "operatingsystem",
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
{{
 ?uri a hito:SoftwareProduct;
      rdfs:label ?label.
 
 OPTIONAL {{?uri rdfs:comment ?comment.}}
 OPTIONAL {{?uri hito:repository ?repository.}}
 OPTIONAL {{?uri hito:homepage ?homepage.}}

 FILTER(LANGMATCHES(LANG(?label),"en")||LANGMATCHES(LANG(?label),""))
}}''',
    "folder": "swp",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "softwareproduct",
    "fields": "(suffix, label, comment, coderepository, homepage)",
    "arrayfields": [5,6]
}

citation = {
    "query": f'''SELECT
REPLACE(STR(?citation),".*/","") as ?suffix
REPLACE(STR(?uri),".*/","") as ?swp_suffix
STR(SAMPLE(?label)) AS ?label
STR(SAMPLE(?comment)) AS ?comment
CONCAT(UCASE(SUBSTR(?p_suffix, 1, 1)), SUBSTR(?p_suffix, 2)) AS ?type
{{
 ?uri a  hito:SoftwareProduct;
     ?p ?citation.
     ?p rdfs:subPropertyOf hito:citation.

  BIND(REPLACE(STR(?p),".*/","") AS ?p_suffix).

 ?citation rdfs:label ?label.
 OPTIONAL {{?citation rdfs:comment ?comment.}}
}}''',
    "folder": "swp",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "citation",
    "fields": "(suffix,swp_suffix, label,comment,type)",
    "arrayfields": []
}

classified = {
    "query": f'''
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dce: <http://purl.org/dc/elements/1.1/>
SELECT
?suffix
REPLACE(STR(?catalogue),".*/","") as ?catalogue_suffix
STR(SAMPLE(?n)) AS ?n
STR(SAMPLE(?label)) AS ?label
STR(SAMPLE(?comment)) AS ?comment
{concat("STR(?synonym)")} AS ?synonyms
{concat("STR(?dct_source)")} AS ?dct_sources
{concat("STR(?dce_source)")} AS ?dce_sources
{{
 ?classified ?p ?catalogue;
             rdfs:label ?label.
 
 OPTIONAL {{?classified rdfs:comment ?comment.}}
 OPTIONAL {{?classified skos:altLabel ?synonym.}}
 OPTIONAL {{?classified hito:memberNr ?n.}}
 OPTIONAL {{?classified dct:source ?dct_source.}}
 OPTIONAL {{?classified dce:source ?dce_source.}}
 ?p rdfs:subPropertyOf hito:catalogue.

 BIND(REPLACE(STR(?classified),".*/","") as ?suffix)
 FILTER(!STRSTARTS(STR(?suffix),"Unknown")) # We treat UnknownX instances as NULL in DB
}}''',
    "folder": "catalogue",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "classified",
    "fields": "(suffix,catalogue_suffix,n,label,comment,synonyms,dct_source,dce_sources)",
    "arrayfields": [5,6,7]
}

# workaround to exclude study citations

citation_has_classified = {
    "query": f'''
SELECT
{suffix("?citation")} AS ?citation_suffix
{suffix("?classified")} AS ?classified_suffix
{{
    ?citation ?p ?classified.
    ?classified a [rdfs:subClassOf hito:Classified].
    ?p rdfs:subPropertyOf hito:classified.
    
    ?swp a hito:SoftwareProduct; ?q ?citation.
}}
GROUP BY ?citation ?classified
HAVING (COUNT(?swp)>=1)''',
    "folder": "relation",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "citation_has_classified",
    "fields": "(citation_suffix,classified_suffix)",
    "arrayfields": []
}
print(citation_has_classified["query"])

classifiedComponent = {
    "query": f'''
SELECT
{suffix("?parent")} AS ?parent_suffix
{suffix("?child")} AS ?child_suffix
{{
 ?child ?p ?parent.
 ?p rdfs:subPropertyOf hito:subClassifiedOf.
 FILTER(?p != hito:supports)
}}''',
    "folder": "relation",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "classified_has_child",
    "fields": "(parent_suffix,child_suffix)",
    "arrayfields": []
}

featureSupportsFunction = {
    "query": f'''
SELECT
{suffix("?feature")} AS ?feature_suffix
{suffix("?function")} AS ?function_suffix
{{
 ?feature hito:supports ?function.
}}''',
    "folder": "relation",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "feature_supports_function",
    "fields": "(feature_suffix,function_suffix)",
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
{"p": "programmingLibrary", "table": "swp_has_programminglibrary", "fieldList": ["swp_suffix", "lib_suffix"]},
{"p": "client", "table": "swp_has_client", "fieldList": ["swp_suffix", "client_suffix"]},
{"p": "databaseSystem", "table": "swp_has_databasesystem", "fieldList": ["swp_suffix", "db_suffix"]}
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

classes = [standard,language,license,programmingLanguage,programmingLibrary,operatingSystem,softwareProduct,classified,classifiedComponent,featureSupportsFunction,citation,citation_has_classified] + list(relations)

