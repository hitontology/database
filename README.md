# HITO Database
Populate the HITO PostgreSQL database and export it back to RDF.
Contains software products and related attributes, such as licenses

## Tunnel Setup

1. Append to ` ~/.ssh/config`:

        Host hitotunnel
        Hostname 139.18.158.56
        ProxyJump star
        LocalForward 5432 localhost:5433
        ControlMaster auto
        ControlPath ~/.ssh/sockets/%r@%h:%p
        User snik

2. Open tunnel via `ssh -fN hitotunnel`
 
3. When finished, close tunnel via `ssh -S ~/.ssh/sockets/snik@139.18.158.56:22 -O exit hitotunnel`

## Import
Import data from the Virtuoso SPARQL endpoint into the PostgreSQL database in two steps:

1. `./download`
2. `./import`

The `download` script converts data from the SPARQL endpoint to .SQL files.
The `import` script executes the SQL statements within those .SQL files on the HITO database.

**Warning**
`./import` *deletes the complete database* without confirmation and replaces it with the new data!

### Requirements
* bash
* Python 3
* psql
* tunnel from the HITO database to localhost

### SPARQL Endpoint Sources
* [HITO](https://hitontology.eu/sparql) including the [Software Ontology](https://www.ebi.ac.uk/ols/ontologies/swo/terms?iri=http://www.ebi.ac.uk/swo/).
* [DBpedia](https://dbpedia.org/sparql)

## Compare
Compare the contents of the SPARQL endpoint to those within the database. 

## Export
Export data back from the database to the SPARQL endpoint.

### Requirements
* bash
* [Ontop](https://ontop-vkg.org/guide/cli.html) with the [PostgreSQL JDBC driver](https://jdbc.postgresql.org/)
* tunnel from the HITO database to localhost

### Setup

Copy `scripts/export/hito.properties.dist` to `scripts/export/hito.properties` and add the database password.

### Usage
    ./export

