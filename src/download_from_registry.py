import os
import neptune.new as neptune


model = neptune.init_model(
    model='MLPROD-REVCLF',
    project='mtszkw/ml-production',
    api_token=os.environ['NEPTUNE_API_TOKEN'],
)

model_versions_df = model.fetch_model_versions_table().to_pandas()
print('All versions:', model_versions_df)

newest_model = model_versions_df[
    model_versions_df["data/git_commit"] == os.environ['GIT_COMMIT']
]
print('Newest version:', newest_model)

print(newest_model.shape)