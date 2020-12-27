FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/saebyuk

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
# For cffi&cryptography's dependency problem + postgresql-dev for psycopg2-binary install problem.
RUN apk update \
    && apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev postgresql-dev  

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
