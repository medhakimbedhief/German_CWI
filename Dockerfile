FROM python:3.9

COPY ./requirements.txt /webapp/requirements.txt

WORKDIR /webapp

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY webapp/* /webapp

LABEL authors="medha"

ENTRYPOINT ["uvicorn"]

CMD ["--host", "0.0.0.0", "app:app" ]
