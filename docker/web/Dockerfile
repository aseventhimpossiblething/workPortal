FROM python:3.7-slim

ENV PIP_VERSION=19.2.2
ENV PIP_TOOLS_VERSION=4.0.0
ENV YARN_VERSION=1.17.3
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get --no-install-recommends --yes install \
    curl netcat procps lsof

RUN python -m venv /venv
RUN /venv/bin/pip install "pip==${PIP_VERSION}" \
                          "pip-tools==${PIP_TOOLS_VERSION}" && \
    /venv/bin/pip install ipython ipdb

RUN mkdir -p /code
WORKDIR /code

COPY requirements.txt requirements.txt
RUN /venv/bin/pip install -r requirements.txt

COPY . /code

ENTRYPOINT gunicorn bdx-api-link:app
