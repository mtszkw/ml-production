import os
import neptune.new as neptune


model = neptune.init_model(
    model='MLPROD-REVCLF',
    project='mtszkw/ml-production',
    api_token=os.environ['NEPTUNE_API_TOKEN'],
)

print("GITHUB SHA:", os.environ["GITHUB_SHA"])
print("GITHUB REF:", os.environ["GITHUB_REF"])

model_versions_df = model.fetch_model_versions_table().to_pandas()
print(model_versions_df)
