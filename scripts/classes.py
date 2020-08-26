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
    "arrayfields": [3],
    "enum": False
}

language = {
    "query": '''SELECT DISTINCT(REPLACE(STR(?uri),"http://dbpedia.org/resource/","")) as ?suffix
{
 ?uri a dbo:Language;
      dbo:iso6391Code [].
}''',
    "folder": "enum",
    "endpoint": "https://dbpedia.org/sparql",
    "table": "Language",
    "fields": "(suffix)",
    "arrayfields": [],
    "enum": True
}

#  SWO is uploaded to the HITO endpoint, they are (transitive) subclasses, not instances
license = {
    "query": '''PREFIX swo: <http://www.ebi.ac.uk/swo/>
SELECT DISTINCT(REPLACE(STR(?uri),"http://www.ebi.ac.uk/swo/license/","")) as ?suffix
#FROM <http://www.ebi.ac.uk/swo/swo.owl/1.7>
{
 ?uri rdfs:subClassOf+ swo:SWO_0000002.
}''',
    "folder": "enum",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "License",
    "fields": "(suffix)",
    "arrayfields": [],
    "enum": True
}

programmingLanguage = {
    "query": '''SELECT DISTINCT(REPLACE(STR(?uri),"http://dbpedia.org/resource/","")) as ?suffix
{
 ?uri a yago:WikicatProgrammingLanguages.
}''',
    "folder": "enum",
    "endpoint": "https://dbpedia.org/sparql",
    "table": "ProgrammingLanguage",
    "fields": "(suffix)",
    "arrayfields": [],
    "enum": True
}

operatingSystem = {
    "query": '''SELECT DISTINCT(REPLACE(STR(?uri),"http://dbpedia.org/resource/","")) as ?suffix
{
 ?uri a hito:OperatingSystem.
}''',
    "folder": "enum",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "OperatingSystem",
    "fields": "(suffix)",
    "arrayfields": [],
    "enum": True
}

softwareProduct = {
    "query": f'''SELECT
{suffix("?uri")} as ?suffix
SAMPLE(STR(?label)) AS ?label
STR(SAMPLE(?comment)) AS ?comment
SAMPLE(?repository) AS ?coderepository
SAMPLE(?homepage) AS ?homepage
{concat(suffix("?client"))} AS ?clients
{concat(suffix("?databaseSystem"))} as ?databaseSystems
{concat(suffix("?language"))} as ?languages
{concat(suffix("?license"))} as ?licenses
{concat(suffix("?operatingSystem"))} as ?operatingSystems
{concat(suffix("?programmingLanguage"))} as ?programmingLanguages
#{concat(suffix("?programmingLibrary"))} as ?programmingLibraries
{{
 ?uri a hito:SoftwareProduct;
      rdfs:label ?label.
 
 OPTIONAL {{?uri rdfs:comment ?comment.}}
 OPTIONAL {{?uri hito:repository ?repository.}}
 OPTIONAL {{?uri hito:homepage ?homepage.}}
 OPTIONAL {{?uri hito:client ?client.}}
 OPTIONAL {{?uri hito:databaseSystem ?databaseSystem.}}
 OPTIONAL {{?uri hito:language ?language.}}
 OPTIONAL {{?uri hito:license ?license.}}
 OPTIONAL {{?uri hito:operatingSystem ?operatingSystem.}}
 OPTIONAL {{?uri hito:programmingLanguage ?programmingLanguage.}}
 #OPTIONAL {{?uri hito:programmingLibrary ?programmingLibrary.}}

 FILTER(LANGMATCHES(LANG(?label),"en")||LANGMATCHES(LANG(?label),""))
}}''',
    "folder": "swp",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "SoftwareProduct",
    "fields": "(suffix, label, comment, coderepository, homepage, clients, databaseSystems, languages, licenses, operatingSystems, programmingLanguages)",
    "arrayfields": [5,6,7,8,9,10],
    "enum": False
}

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
    "arrayfields": [],
    "enum": False
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
    "table": "Classified",
    "fields": "(suffix,catalogue_suffix,n,label,comment,synonyms,dct_source,dce_sources)",
    "arrayfields": [5,6,7],
    "enum": False
}

classifiedComponent = {
    "query": f'''
SELECT
{suffix("?parent")} AS ?parent_suffix
{suffix("?child")} AS ?child_suffix
{{
 ?child ?p ?parent.
 ?p rdfs:subPropertyOf hito:subClassifiedOf. 
}}''',
    "folder": "relation",
    "endpoint": "https://hitontology.eu/sparql",
    "table": "classified_has_child",
    "fields": "(parent_suffix,child_suffix)",
    "arrayfields": [],
    "enum": False
}

# Properties candidates for the query were determined via:
# SELECT DISTINCT ?p {?s a hito:SoftwareProduct; ?p ?o.}
# Of those we only use properties that don't have their own database table in the first query for simpler mapping and to reduce OPTIONAL statements.

relationData = [
{"p": "softwareProductComponent", "table": "swp_has_child", "fieldList": ["parent_suffix", "child_suffix"]},
{"p": "interoperability", "table": "swp_has_interoperabilitystandard", "fieldList": ["swp_suffix", "io_suffix"]},
#{"p": "language", "table": "swp_has_language", "fieldList": ["swp_suffix", "lang_suffix"]},
#{"p": "license", "table": "swp_has_license", "fieldList": ["swp_suffix", "license_suffix"]},
#{"p": "operatingSystem", "table": "swp_has_operatingsystem", "fieldList": ["swp_suffix", "os_suffix"]},
#{"p": "programmingLanguage", "table": "swp_has_programminglanguage", "fieldList": ["swp_suffix", "plang_suffix"]},
#{"p": "programmingLibrary", "table": "swp_has_programminglibrary", "fieldList": ["swp_suffix", "lib_suffix"]}
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
    "arrayfields": [],
    "enum": False
}
, relationData)

classes = [standard,language,license,programmingLanguage,operatingSystem,softwareProduct,classified,classifiedComponent,citation] + list(relations)

