# python:alpine would work as well and is smaller but python:slim is also used in the database frontend.
FROM python:slim

LABEL	maintainer="Konrad Höffner" \
	maintainer.email="konrad.hoeffner(at)imise.uni-leipzig.de" \
	maintainer.organization="Universität Leipzig: Institut für Medizinische Informatik, Statistik und Epidemiologie (IMISE)" \
	maintainer.repo="https://github.com/hitontology/database"

COPY ./import/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt --disable-pip-version-check --no-cache-dir

# Set and create output folder
ENV SQL_OUTPUT_BASE_DIR=/sql
WORKDIR ${SQL_OUTPUT_BASE_DIR}

# Copy source code
WORKDIR /usr/src/app
COPY ./import/classes.py .
COPY ./import/download.py .
COPY ./import/base ./base

ENV HITO_FILE=${HITO_FILE:-/rdf/hito.nt}
ENV SWO_FILE=${SWO_FILE:-/rdf/license.ttl}
#ENV DBPEDIA_SPARQL_ENDPOINT
CMD ["python","download.py"]
