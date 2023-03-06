FROM python:3.9-slim-bullseye

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


# install git - required by dbt
RUN apt-get update \
    && apt-get install -y git wget libaio1 unzip libssl-dev cmake make curl libpq-dev

# Creates virtual environment
WORKDIR /
RUN python3 -m venv /opt/venv

# Set Python path
ENV PATH="/opt/venv/bin:${PATH}"

# Oracle client required if we need to extract data from on-prem Oracle 
# Installing Oracle instant client. 
# https://blogs.oracle.com/opal/post/part-1-docker-for-oracle-database-applications-in-nodejs-and-python
WORKDIR /opt/oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
    unzip instantclient-basiclite-linuxx64.zip && \
    rm -f instantclient-basiclite-linuxx64.zip && \
    cd instantclient* && \
    rm -f *jdbc* *occi* *mysql* *jar uidrvci genezi adrci && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

# innstall python packages
COPY requirements.txt .
RUN python -m pip install pip --upgrade && \
    python -m pip install -r requirements.txt

# Copy app and configs
COPY . /app

# install dbt packages
WORKDIR /app/dbt
RUN dbt deps

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
