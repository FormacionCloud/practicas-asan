FROM python:3.12-slim
RUN pip install --no-cache-dir boto3
COPY aggregator.py /app/aggregator.py
CMD ["python", "/app/aggregator.py"]
