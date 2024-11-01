# 
FROM python:3.9
RUN mkdir -p /app
# 
WORKDIR /app
COPY *.py /app
# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
EXPOSE 8080

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
ENTRYPOINT [ "python", "main.py" ]