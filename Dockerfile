FROM alpine:3.8

RUN mkdir -p /app

COPY requirements.txt /app/requirements.txt

#RUN apk add --no-cache python3 py3-pip

RUN pip3 install -r /app/requirements.txt

COPY ./app/*.py /app
                 
WORKDIR /app

EXPOSE 9091

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9091"]
