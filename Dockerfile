FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/saebyuk


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN echo 'python was not a problem'

# install dependencies
RUN pip install --upgrade pip
# For cffi&cryptography's dependency problem + postgresql-dev for psycopg2-binary install problem.
RUN apk update \
    && apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev postgresql-dev  


COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN echo 'pip was not a problem'

COPY ./app/entrypoint.sh .
RUN echo 'shebang was not a problem'


# copy project
COPY . .
RUN echo 'copying was not a problem'

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
