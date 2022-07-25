FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set work directory
WORKDIR /project

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /project/
RUN pip install -r requirements.txt

# copy project
COPY . /project/
