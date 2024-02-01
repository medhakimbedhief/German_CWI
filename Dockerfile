FROM python:3.9

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /webapp/requirements.txt

WORKDIR /webapp

<<<<<<< HEAD
=======
RUN python -m pip install --upgrade pip
>>>>>>> refs/remotes/origin/main
RUN pip install -r requirements.txt

COPY webapp/* /webapp

LABEL authors="medha"

ENTRYPOINT ["uvicorn"]

<<<<<<< HEAD
CMD ["--host", "0.0.0.0", "main:app" ]
=======
CMD ["--host", "0.0.0.0", "app:app" ]
>>>>>>> refs/remotes/origin/main
