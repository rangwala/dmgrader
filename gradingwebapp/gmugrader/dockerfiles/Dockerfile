FROM python:3.7.0
ENV PYTHONUNBUFFERED 1
RUN mkdir /cs491
ADD dmgrader.tar /cs491/
WORKDIR /cs491/dmgrader/gradingwebapp/gmugrader
RUN pip install -r requirements.txt 
EXPOSE 8000
