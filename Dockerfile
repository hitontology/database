FROM python:alpine

LABEL	maintainer="Konrad Höffner" \
	maintainer.email="konrad.hoeffner(at)imise.uni-leipzig.de" \
	maintainer.organization="Universität Leipzig: Institut für Medizinische Informatik, Statistik und Epidemiologie (IMISE)" \
	maintainer.repo="https://github.com/hitontology/database"


COPY ./import/py/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt --disable-pip-version-check --no-cache-dir

# Copy source code
WORKDIR /usr/src/app
COPY ./import/py/classes.py .
COPY ./import/py/download.py .
COPY ./import/base ./base

# Download from the SPARQL endpoint
ENV SQL_OUTPUT_BASE_DIR=/tmp/sql
RUN mkdir /tmp/sql \
 && mkdir -p /sql \
 && python download.py \
 && cat base/schema.sql base/catalogues.sql /tmp/sql/catalogue/classified.sql /tmp/sql/attribute/*.sql  /tmp/sql/swp/softwareproduct.sql /tmp/sql/swp/citation.sql /tmp/sql/relation/*.sql > /sql/hito.sql \
 && wc -l /sql/hito.sql
