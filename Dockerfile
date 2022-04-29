FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev && \
    pip install psycopg2-binary

CMD echo "I win"

WORKDIR /app
COPY ./app.py /app/app.py
COPY ./requirement.txt /app/requirement.txt
COPY ./static /app/static
COPY ./templates /app/templates
RUN pip install -r /app/requirement.txt
EXPOSE 5000
CMD ["python3", "/app/app.py"]