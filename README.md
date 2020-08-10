# HITO Database
Populate the HITO PostgreSQL database.
Contains software products and related attributes, such as licenses

## Requirements
* bash
* Python 3
* psql
* tunnel from the HITO database to localhost

## Usage
```
./transform
./import
```
**Warning**
`./import` *deletes the complete database* without confirmation and replaces it with the new data!

## SPARQL Endpoint Sources
* [HITO](https://hitontology.eu/sparql) including the [Software Ontology](https://www.ebi.ac.uk/ols/ontologies/swo/terms?iri=http://www.ebi.ac.uk/swo/).
* [DBpedia](https://dbpedia.org/sparql)
