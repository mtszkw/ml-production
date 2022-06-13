import os
import neptune.new as neptune


model = neptune.init_model(
    model='MLPROD-REVCLF',
    project='mtszkw/ml-production',
    api_token=os.environ['NEPTUNE_API_TOKEN'],
)

model_versions_df = model.fetch_model_versions_table().to_pandas()
print(model_versions_df)
