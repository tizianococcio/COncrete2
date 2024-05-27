FROM python:3.10

WORKDIR /data_source

# Copy requirements.txt from the data_source directory
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "producer.py"]
