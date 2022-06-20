FROM python:3.9.6-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV PIP_NO_CACHE_DIR false

WORKDIR /app/
COPY requirements.txt /app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "feeder.wsgi", ":8000"]