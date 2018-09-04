"""
This provides a sample workflow to kick-off a parametric study using the brute force algorithm
The brute force algorithm will exhaustively simulate all the possible combinations of the
measures -

e.g.
if:
 2 options for lighting power density,
 2 options for window wall ratio,
 2 options for heating efficiency

The total number of possible combinations is 2 x 2 x 2 = 8 - so this script will run 8 simulations.

Enter the project_api_key - which link to the project that you wish to host your parametric study.

Enter the model_api_key if you wish to use a model on the BuildSim Cloud as seed model,
or you can specify local_file_dir variable to submit a seed model (you need to switch the model_api_key to None or ''
in order to submit the model from local).

"""

import BuildSimHubAPI as bsh_api
import pandas as pd
import numpy as np
from sklearn import linear_model
import scipy.optimize as opt

# 1. set your folder key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = '03b7947b-38d4-4d92-8c6d-b826166e937d'


# Helper functions
# A helper method for pretty-printing linear models
def pretty_print_linear(coefs, names=None, sort=False):
    if names is None:
        names = ["X%s" % x for x in range(len(coefs))]
    lst = zip(coefs, names)
    if sort:
        lst = sorted(lst, key=lambda x: -np.abs(x[0]))
    return " + ".join("%s * %s" % (round(coef, 3), name)
                      for coef, name in lst)


bsh = bsh_api.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
# if the seed model is on the buildsim cloud - add model_api_key to the new_parametric_job function
# Get the EUI results

# Define EEMs
measure_list = list()

wwrn = bsh_api.measures.WindowWallRatio(orientation="N")
wwrn.set_min(0.3)
wwrn.set_max(0.6)
measure_list.append(wwrn)

wwrs = bsh_api.measures.WindowWallRatio(orientation="S")
wwrs.set_min(0.3)
wwrs.set_max(0.6)
measure_list.append(wwrs)

wwrw = bsh_api.measures.WindowWallRatio(orientation="W")
wwrw.set_min(0.3)
wwrw.set_max(0.6)
measure_list.append(wwrw)

wwre = bsh_api.measures.WindowWallRatio(orientation="E")
wwre.set_min(0.3)
wwre.set_max(0.6)
measure_list.append(wwre)

lpd = bsh_api.measures.LightLPD('ip')
lpd.set_min(0.6)
lpd.set_max(1.2)
measure_list.append(lpd)

chillerEff = bsh_api.measures.CoolingChillerCOP()
chillerEff.set_min(3.5)
chillerEff.set_max(5.5)
measure_list.append(chillerEff)

heatEff = bsh_api.measures.HeatingEfficiency()
heatEff.set_min(0.8)
heatEff.set_max(0.95)
measure_list.append(heatEff)

results = bsh.parametric_results(project_api_key, model_api_key)
# Collect results
result_dict = results.net_site_eui()
result_unit = results.last_parameter_unit

for i in range(len(result_dict)):
   tempstr = result_dict["value"]

dict = {}
for key in result_dict:
    if key == "model":
        templist = result_dict[key]
        tempdict = {}
        for i in range(len(templist)):
            tempstr = result_dict["model"][i]
            templist = tempstr.split(',')
            for j in range(len(templist)):
                pair = templist[j].split(': ')
                if pair[0] not in tempdict:
                    tempdict[pair[0]] = []
                tempdict[pair[0]].append(pair[1])
        for subkey in tempdict:
            dict[subkey] = tempdict[subkey]
    elif key != 'model_plot':
        dict[key] = result_dict[key]

df = pd.DataFrame(dict)
# Training code starts from here
y = df.loc[:, 'value']
x = df.loc[:, df.columns != 'value']
column_head = list(x)
# train a regression model
alg = linear_model.LinearRegression()
alg.fit(x, y)
print('Linear regression model: ' + str(alg.intercept_) + ' + ' + pretty_print_linear(alg.coef_))


def fun(x_pred): return alg.predict([x_pred])


def bounds(col_head):
    col_head = col_head.strip()
    for measure in measure_list:
        if measure.measure_name == col_head:
            return measure.get_range()


def col_max(col_head):
    col_head = col_head.strip()
    for measure in measure_list:
        if measure.measure_name == col_head:
            return measure.get_max()


bounds = [bounds(col_head) for col_head in column_head]
X = np.array([[col_max(col_head)] for col_head in column_head])
X.reshape(1, -1)
res = opt.minimize(fun, X, bounds=bounds, options={'disp': True})

print("Optimized")
print(column_head)
print(res.x)

target_val = alg.predict([res.x])
print(target_val)

# Let's run the single model with the above values
for i in range(len(measure_list)):
    measure = measure_list[i]

    # search for the index in the column
    for j in range(len(column_head)):
        col_head = column_head[j].strip()
        if measure.measure_name == col_head:
            measure.set_data(res.x[j])
            break

model = bsh.model_results(project_api_key, model_api_key)
model_id = model.apply_measures(measure_list)

new_sj = bsh.new_simulation_job(project_api_key)
result = new_sj.run_model_simulation(model_id, track=True)
print(result.net_site_eui())
