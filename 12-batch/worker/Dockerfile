FROM python:3.12-slim
RUN pip install --no-cache-dir boto3
COPY worker.py /app/worker.py
CMD ["python", "/app/worker.py"]
