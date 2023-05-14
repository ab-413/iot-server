FROM python:3.10

WORKDIR /app/

ENV PYTHONPATH=/app

COPY ./app /app/app
COPY ./requirements.txt /app/

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080" ]