FROM python:3
WORKDIR /usr/src/app

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN apt-get install -y default-libmysqlclient-dev
RUN pip3 install mysqlclient

COPY . .

EXPOSE 8000

ENTRYPOINT ["dockerize", "-wait", "tcp://mysql_service:3306", "-timeout", "20s"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "playde_server.wsgi:application"]
