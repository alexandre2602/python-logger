FROM alpine

COPY . /app

WORKDIR /app

RUN apk add --no-cache py3-pip && pip3 install -r requirements.txt

#RUN mv app-full.py app.py

CMD python3 -m flask run --host 0.0.0.0
