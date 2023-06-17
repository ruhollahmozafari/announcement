### Build and install packages
FROM python:3.8

# Update base container install
RUN apt-get update
RUN apt-get upgrade -y

# Add unstable repo to allow us to access latest GDAL builds
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install libgdal-dev -y
# RUN apt install python3-dev libpq-dev
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary

COPY . /app
WORKDIR /app


EXPOSE 8000
ENV PYTHONUNBUFFERED 1
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

