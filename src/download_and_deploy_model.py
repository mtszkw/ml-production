import os
from pathlib import Path

import boto3
import botocore
import neptune.new as neptune
from sagemaker.tensorflow import TensorFlowModel


def export_to_s3(model_archive: Path, region: str, bucket_name: str):
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError:
        print(f"Bucket {bucket_name} not found, creating new one")
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region})

    s3_path = f"s3://{bucket_name}/{model_archive}"
    print(f"Uploading model to: {s3_path}")
    s3_client.upload_file(model_archive, bucket_name, model_archive)
    return s3_path


def deploy_sagemaker_endpoint_from_s3(model_s3_path: str):
    print("Deploying TensorFlow model to a SageMaker Endpoint...")
    model = TensorFlowModel(
        model_data=model_s3_path,
        role="SageMakerExecutor",
        framework_version="2.6"
    )
    predictor = model.deploy(initial_instance_count=1, instance_type='ml.c5.xlarge')


if __name__ == "__main__":
    model = neptune.init_model(
        model='MLPROD-REVCLF',
        project='mtszkw/ml-production',
        api_token=os.environ['NEPTUNE_API_TOKEN'],
    )

    # Get all registered models and find the one with correct GIT_COMMIT
    model_versions_df = model.fetch_model_versions_table().to_pandas()
    # print('All versions:', model_versions_df)
    newest_model = model_versions_df.iloc[0]
    print('Newest version:', newest_model)
    version_id = newest_model["sys/id"]

    # Download artifacts for the model
    model_version = neptune.init_model_version(
        project='mtszkw/ml-production',
        api_token=os.environ['NEPTUNE_API_TOKEN'],
        version=version_id
    )
    print(f"Downloading model binary to model_{version_id}.tar.gz")
    model_version["model/binary"].download(f"model_{version_id}.tar.gz")

    # Upload model binary to S3
    s3_path = export_to_s3(
        model_archive=f"model_{version_id}.tar.gz",
        region=os.environ['MODEL_AWS_REGION'],
        bucket_name=os.environ['MODEL_AWS_BUCKET'])
    
    # Deploy SageMaker Endpoint from S3 binary
    # deploy_sagemaker_endpoint_from_s3(model_s3_path=s3_path)
    
    # and officially promote the model to production
    # model_version.change_stage("production")
    
    model.stop()