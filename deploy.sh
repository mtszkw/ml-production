#!/bin/bash

MODEL_S3_PATH="s3://mateusz-kwasniak/review_classifier.tar.gz" \
  python3 deploy_to_sagemaker.py