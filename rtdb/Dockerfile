# pull official base image
FROM python:3.11.4



# Updating the os
RUN apt update 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copying requirement file
COPY ./requirements.txt ./

RUN apt-get install -y pkg-config
# Upgrading pip version
RUN pip3 install --upgrade pip setuptools wheel 

# Installing dependencies

RUN pip3 install --no-cache-dir -r ./requirements.txt

# set environment variables

COPY . /home/rtdb

WORKDIR /home/rtdb
