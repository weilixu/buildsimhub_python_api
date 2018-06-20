"""
This sample file demonstrate how to download a model from BuildSimHub using API

"""

import BuildSimHubAPI as bshapi

# project_key can be found in every project (click the information icon next to project name)
project_key = "f98aadb3-254f-428d-a321-82a6e4b9424c"
# model_key can be found in each model information bar
model_key = "1-146-428"

# initialize the client
bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
results = bsh.model_results(project_key, model_key)
print(results.download_model())


