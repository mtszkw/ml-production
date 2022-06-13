import os
from sagemaker.tensorflow import TensorFlowModel


MODEL_S3_PATH = os.environ["MODEL_S3_PATH"]

print("Deploying TensorFlow model to a SageMaker Endpoint...")

model = TensorFlowModel(
    model_data=MODEL_S3_PATH,
    role="SageMakerExecutor",
    framework_version="2.6"
)

predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.c5.xlarge')