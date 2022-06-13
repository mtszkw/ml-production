import os
import json

import neptune.new as neptune


try:
    model = neptune.init_model(
        name="Review Classification",
        key="REVCLF",
        project="mtszkw/ml-production",
        api_token=os.environ["NEPTUNE_API_TOKEN"],
    )
except neptune.exceptions.NeptuneModelKeyAlreadyExistsError:
    print("Model key already exists, skipping...")


model_version = neptune.init_model_version(
    model='MLPROD-REVCLF',
    project='mtszkw/ml-production',
    api_token=os.environ['NEPTUNE_API_TOKEN'],
)
model_version["github_sha"] = os.environ['GITHUB_SHA']
model_version["github_ref"] = os.environ['GITHUB_REF']
model_version["model/parameters"].upload('parameters.json')
model_version["model/training_code"].upload('src/train.py')
model_version["model/binary"].upload(os.environ['MODEL_ARCHIVE_OUTPUT_PATH'])

model_version.stop()



model.stop()


# run.stop()