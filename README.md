# HITO Database
Populate the HITO PostgreSQL database.
Contains software products and related attributes, such as licenses

## Requirements
* bash
* Python 3
* psql
* tunnel from the HITO database to localhost

## Tunnel Setup

1. Append to ` ~/.ssh/config`:

    Host hitotunnel
    Hostname 139.18.158.56
    ProxyJump  star
    LocalForward 5432 localhost:5433
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
    User snik

2. Open tunnel via `ssh -fN hitotunnel`
 
3. When finished, close tunnel via `ssh -S ~/.ssh/sockets/snik@139.18.158.56:22 -O exit hitotunnel`

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
