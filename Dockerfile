FROM python:3.12-slim

LABEL maintainer="kuzikbv2509@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN addgroup --system my_group && adduser --system --ingroup my_group my_user

RUN chown -R my_user:my_group /app

USER my_user

EXPOSE 8000

CMD ["gunicorn", "theatre_service.wsgi:application", "--bind", "0.0.0.0:8000"]
