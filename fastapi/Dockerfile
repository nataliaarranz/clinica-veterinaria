FROM tiangolo/uvicorn-gunicorn

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

COPY . /fastapi

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]