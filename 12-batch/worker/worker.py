#!/usr/bin/env python3
import os
import json
import boto3

s3 = boto3.client("s3")

BUCKET = os.environ["BUCKET"]
INPUT_KEY = os.environ["INPUT_KEY"]       # "input/numbers.json"
OUTPUT_PREFIX = os.environ["OUTPUT_PREFIX"]  # "output/"
INDEX = int(os.environ["AWS_BATCH_JOB_ARRAY_INDEX"]) # Insertado por el trabajo array de AWS Batch


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def main():
    # Leer la lista de números
    obj = s3.get_object(Bucket=BUCKET, Key=INPUT_KEY)
    numbers = json.loads(obj["Body"].read())

    number = numbers[INDEX]
    result = {"number": number, "is_prime": is_prime(number)}
    print(f"[{INDEX}] {number} -> prime={result['is_prime']}")

    # Escribir resultado
    out_key = f"{OUTPUT_PREFIX}{INDEX}.json"
    s3.put_object(Bucket=BUCKET, Key=out_key, Body=json.dumps(result))


if __name__ == "__main__":
    main()
