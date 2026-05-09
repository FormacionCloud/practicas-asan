#!/usr/bin/env python3
import os
import json
import boto3

s3 = boto3.client("s3")

BUCKET = os.environ["BUCKET"]
OUTPUT_PREFIX = os.environ["OUTPUT_PREFIX"]  # "output/"
ARRAY_SIZE = int(os.environ["ARRAY_SIZE"])


def main():
    primes = []
    non_primes = []

    for i in range(ARRAY_SIZE):
        obj = s3.get_object(Bucket=BUCKET, Key=f"{OUTPUT_PREFIX}{i}.json")
        result = json.loads(obj["Body"].read())
        if result["is_prime"]:
            primes.append(result["number"])
        else:
            non_primes.append(result["number"])

    summary = {
        "primos": sorted(primes),
        "no_primos": sorted(non_primes),
        "total": ARRAY_SIZE,
    }

    print(json.dumps(summary, indent=2))

    s3.put_object(
        Bucket=BUCKET,
        Key=f"{OUTPUT_PREFIX}summary.json",
        Body=json.dumps(summary, indent=2),
    )
    print(f"Fichero guardado en s3://{BUCKET}/{OUTPUT_PREFIX}summary.json")


if __name__ == "__main__":
    main()
