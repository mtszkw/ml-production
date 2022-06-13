#!/bin/bash

echo "Configuring virtual environment..."
python3 -m venv ./env && . ./env/bin/activate && pip3 install -r requirements.txt

echo "Executing ML pipeline..."
  MODEL_AWS_BUCKET="mateusz-kwasniak" \
  MODEL_AWS_REGION="eu-west-1" \
  MODEL_EXPORT_DIRECTORY="$(pwd)/bin/review_classifier/1" \
  MODEL_ARCHIVE_OUTPUT_PATH="review_classifier.tar.gz" \
  python3 train_model.py