FROM python:3.8-alpine

# Creating folder
RUN mkdir /opt/podio_api_delete
COPY . /opt/podio_api_delete
WORKDIR /opt/podio_api_delete

# Installing dependencies
RUN apk update
RUN apk add --no-cache py3-pip python3-dev

# Getting pypodio2 library
RUN pip install -e git+https://github.com/gbvsilva/podio-py.git#egg=podio-py

# Installing Python dependencies
RUN pip install --no-cache-dir psycopg2-binary requests

# Cleaning cache
RUN apk del git && rm -rf /var/cache/apk/*

# Setting entrypoint
CMD ["-u", "/opt/podio_api/main.py"]
ENTRYPOINT [ "python3" ]
