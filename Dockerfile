FROM python:3.9.7-slim-buster

ENV APP_DIR /app

RUN \
  apt-get update && \
  apt install -y build-essential && \
  apt install -y python3-dev python3-pip && \
  pip install --upgrade pip setuptools

WORKDIR ${APP_DIR}

ADD setup.py ${APP_DIR}/
ADD src ${APP_DIR}/src
ADD tests ${APP_DIR}/tests
RUN pip install -e '.[all]'

CMD python -m space_invaders
