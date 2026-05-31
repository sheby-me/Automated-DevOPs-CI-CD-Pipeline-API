FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN pip install django gitpython

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]