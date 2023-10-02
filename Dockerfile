FROM python:3.9.10

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/
EXPOSE 8080
RUN pip install -r requirements.txt


