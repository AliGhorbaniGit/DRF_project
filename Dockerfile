FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing .pyc files  
ENV PYTHONUNBUFFERED 1         # Ensures output is sent straight to terminal

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/