FROM python:3.12

WORKDIR /backend

RUN pip install -r requirements.txt
RUN pip install mysqlclient
RUN pip install drf-yasg

COPY . /backend

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]