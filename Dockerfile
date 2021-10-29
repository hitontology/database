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

# Download from the SPARQL endpoint
ENV SQL_OUTPUT_BASE_DIR=/sql/
RUN python download.py

