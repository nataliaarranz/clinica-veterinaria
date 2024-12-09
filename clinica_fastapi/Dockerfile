FROM tiangolo/uvicorn-gunicorn

RUN mkdir /clinica_fastapi
WORKDIR /clinica_fastapi

COPY requirements.txt /clinica_fastapi


RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["uvicorn", "clinica_fastapi.server:app", "--host", "0.0.0.0", "--port", "8000"]