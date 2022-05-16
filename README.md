## :warning: **The HITO Database is neither used nor maintained anymore. It was only used together with the [Database Frontend](https://github.com/hitontology/database-frontend/), which is archived as well.**
This repository has been archived on 2022-05-16.

# HITO Database
Populate the HITO PostgreSQL database and export it back to RDF.
Contains software products and related attributes, such as licenses

## Tunnel Setup

1. Append to ` ~/.ssh/config`:

        Host hitotunnel
        Hostname datrav.uni-leipzig.de
        ProxyJump star
        LocalForward 5432 localhost:55432
        ControlMaster auto
        ControlPath ~/.ssh/sockets/%r@%h:%p
        User root

2. Open tunnel via `ssh -fN hitotunnel`
 
3. When finished, close tunnel via `ssh -S ~/.ssh/sockets/root@datrav.uni-leipzig.de:22 -O exit hitotunnel`

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

## Export
Export data back from the database to the SPARQL endpoint.

### Requirements
* bash
* [Ontop](https://ontop-vkg.org/guide/cli.html) with the [PostgreSQL JDBC driver](https://jdbc.postgresql.org/)
* tunnel from the HITO database to localhost

### Setup

Copy `scripts/export/hito.properties.dist` to `scripts/export/hito.properties` and add the database password.

### Workflow

    cd diff
    ./prepare
    ./compare
    ./diff

Or even better, instead of `./diff` run `vimdiff export/output/all.ttl /path/to/my/ontology/swp.ttl` from the base directory and then you can directly push the changes into the ontology repository.
When the ontology repository is updated, go on the server, run `git pull` in the `ontology` directory and then in the docker directory:

    docker-compose down -v
    docker-compose build --no-cache
    docker-compose up
