FROM python:latest

MAINTAINER Serhii Plys serhiiplys@gmail.com

COPY . /web_hw3

WORKDIR /web_hw3

RUN pip install flask

ENTRYPOINT ["python"]
CMD ["example_hw3.py"]