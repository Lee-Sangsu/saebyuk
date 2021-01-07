FROM python:3.8.3-alpine as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
# COPY . .

# For cffi&cryptography's dependency problem + postgresql-dev for psycopg2-binary install problem.
RUN apk update \
    && apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev postgresql-dev  

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# COPY ./entrypoint.sh .
# copy project
COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "saebyuk.wsgi:application"]  
# ENTRYPOINT [ "/usr/src/app/entrypoint.prod.sh" ]