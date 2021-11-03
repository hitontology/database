# alpine includes netcat for wait-for
FROM python:alpine

LABEL	maintainer="Konrad Höffner" \
	maintainer.email="konrad.hoeffner(at)imise.uni-leipzig.de" \
	maintainer.organization="Universität Leipzig: Institut für Medizinische Informatik, Statistik und Epidemiologie (IMISE)" \
	maintainer.repo="https://github.com/hitontology/database"

ENV SQL_OUTPUT_BASE_DIR=/tmp/sql
ENV SQL_FILE_COMPLETE=/sql/hito.ttl
RUN mkdir -p ${SQL_OUTPUT_BASE_DIR} \
 && mkdir -p /sql

COPY ./import/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt --disable-pip-version-check --no-cache-dir

# Copy source code
WORKDIR /usr/src/app
COPY ./import/classes.py .
COPY ./import/download.py .
COPY ./import/wait-for .
COPY ./import/base ./base

#CMD ["python","download.py"]
CMD ["./wait-for","virtuoso:8890","--","python","download.py"]
