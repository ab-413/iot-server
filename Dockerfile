FROM python:3.10-alpine

WORKDIR /app/

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./app /app/app
COPY ./requirements.txt /app/

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--app-dir", "/app/app" ]
