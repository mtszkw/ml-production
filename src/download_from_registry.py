import os
from pathlib import Path

import boto3
import botocore
import neptune.new as neptune


def export_to_s3(model_archive: Path, region: str, bucket_name: str):
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError:
        print(f"Bucket {bucket_name} not found, creating new one")
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region})

    print(f"Uploading model to: s3://{bucket_name}/{model_archive}")
    s3_client.upload_file(model_archive, bucket_name, model_archive)


if __name__ == "__main__":
    model = neptune.init_model(
        model='MLPROD-REVCLF',
        project='mtszkw/ml-production',
        api_token=os.environ['NEPTUNE_API_TOKEN'],
    )

    model_versions_df = model.fetch_model_versions_table().to_pandas()
    print('All versions:', model_versions_df)

    newest_model = model_versions_df[
        model_versions_df["data/git_commit"] == os.environ['GIT_COMMIT']
    ]

    print('Newest version:', newest_model)

    for _, model_version in newest_model.iterrows():
        version_id = model_version["sys/id"]
        model_version = neptune.init_model_version(
            project='mtszkw/ml-production',
            api_token=os.environ['NEPTUNE_API_TOKEN'],
            version=version_id
        )
        print(f"Downloading model binary to model_{version_id}.tar.gz")
        model_version["model/binary"].download(f"model_{version_id}.tar.gz")

        export_to_s3(
            model_archive=f"model_{version_id}.tar.gz",
            region=os.environ['MODEL_AWS_REGION'],
            bucket_name=os.environ['MODEL_AWS_BUCKET'])
    
    model.stop()