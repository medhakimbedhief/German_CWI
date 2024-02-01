FROM python:3.9

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /webapp/requirements.txt

WORKDIR /webapp

RUN pip install -r requirements.txt

COPY webapp/* /webapp

LABEL authors="medha"

ENTRYPOINT ["uvicorn"]

CMD ["--host", "0.0.0.0", "main:app" ]