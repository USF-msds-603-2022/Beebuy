FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

CMD echo "I win"

WORKDIR /app
COPY ./flask_test.py /app/flask_test.py
COPY ./requirement.txt /app/requirement.txt
COPY ./static /app/static
COPY ./templates /app/templates
RUN pip install -r /app/requirement.txt
EXPOSE 5000
CMD ["python3", "/app/flask_test.py"]

