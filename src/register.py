import os
import json

import neptune.new as neptune

model = neptune.init_model(
    name="Review Classification",
    key="REVCLF",
    project="mtszkw/ml-production",
    api_token=os.environ["NEPTUNE_API_TOKEN"],
)

# run = neptune.init(
    # project="mtszkw/ml-production",
    # api_token=os.environ["NEPTUNE_API_TOKEN"],
# )

model_version = neptune.init_model_version(model="MLPROD-REVCLF")
model_version["parameters"].upload('parameters.json')
model_version["training_code"].upload('src/train.py')
model_version.stop()

# model_version["model/binary"].upload()

model.stop()


# run.stop()