import json
import os

import neptune.new as neptune


try:
    model = neptune.init_model(
        name="Review Classification",
        key="REVCLF",
        project="mtszkw/ml-production",
        api_token=os.environ["NEPTUNE_API_TOKEN"],
    )
    model.stop()
except neptune.exceptions.NeptuneModelKeyAlreadyExistsError:
    print("Model key already exists, skipping...")

# TODO: check if version with PULL_REQUEST_ID already exists

model_version = neptune.init_model_version(
    model='MLPROD-REVCLF',
    project='mtszkw/ml-production',
    api_token=os.environ['NEPTUNE_API_TOKEN'],
)

# Save metrics
with open('metrics.json') as fp:
    metrics = json.load(fp)
    model_version["model/test_accuracy"] = metrics['test_accuracy']
    model_version["model/test_loss"] = metrics['test_loss']
model_version["model/metrics"].upload('metrics.json')

# Save other parameters
model_version["data/pull_request_id"] = os.getenv('PULL_REQUEST_ID', '-1')
model_version["model/parameters"].upload('parameters.json')
model_version["model/training_code"].upload('src/train.py')
model_version["model/binary"].upload(os.environ['MODEL_ARCHIVE_OUTPUT_PATH'])

model_version.stop()
