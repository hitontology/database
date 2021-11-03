# HITO SPARQL to SQL downloader
Uses SPARQL queries to get the current state of HITO from the given SPARQL endpoint and transforms the relevant parts to SQL queries to fill a PostgreSQL databse. Executing the SQL files will cause all existing data in the database to be deleted.

## Environment variables

* HITO_SPARQL_ENDPOINT URL of a SPARQL endpoint that contains HITO. Defaults to `https://hitontology.eu/sparql`.
* DBPEDIA_SPARQL_ENDPOINT URL of a SPARQL endpoint contains DBpedia. Defaults to `https://dbpedia.org/sparql`.
* SQL_OUTPUT_BASE_DIR directory where the SQL files are written. Defaults to `./tmp/`.
