FROM python:3.12-slim
LABEL maintainer="kuzikbv2509@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN addgroup --system my_group && \
    adduser --system --ingroup my_group my_user

USER my_user
