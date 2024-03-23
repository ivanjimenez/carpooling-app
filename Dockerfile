FROM alpine:3.8

RUN mkdir -p /app

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
                 
EXPOSE 9091

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9091"]
