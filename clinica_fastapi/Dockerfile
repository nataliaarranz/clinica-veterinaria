FROM tiangolo/uvicorn-gunicorn

RUN mkdir /fastapi

COPY ./clinica_fastapi/requirements.txt .

WORKDIR /clinica_fastapi

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

COPY . /clinica_fastapi

EXPOSE 8000

CMD ["uvicorn", "clinica_fastapi.server:app", "--host", "0.0.0.0", "--port", "8000"]