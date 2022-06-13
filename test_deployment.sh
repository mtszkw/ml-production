#!/bin/bash

export MODEL_ENDPOINT_NAME=$(aws sagemaker list-endpoints | jq -r ".Endpoints[].EndpointName")

aws sagemaker-runtime invoke-endpoint \
  --endpoint-name $MODEL_ENDPOINT_NAME \
  --body "{\"instances\": [\"absolutely the best\"]}" \
  --content-type application/json \
  --accept application/json \
  --cli-binary-format raw-in-base64-out \
  results && cat results

aws sagemaker-runtime invoke-endpoint \
  --endpoint-name $MODEL_ENDPOINT_NAME \
  --body "{\"instances\": [\"total crap, nightmare and misunderstanding\"]}" \
  --content-type application/json \
  --accept application/json \
  --cli-binary-format raw-in-base64-out \
  results && cat results