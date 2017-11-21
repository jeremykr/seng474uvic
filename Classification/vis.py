import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.interpolate import spline
from scipy.stats import pearsonr
from utils import Utils

houses = Utils.get_house_data("../RemaxScrape/remaxVanDataset.json")
print(len(houses))

# Do stuff here

#for i in range(len(houses[0])):
#    pearson_scores.append([attribs[i]] + list(pearsonr(prices, [h[i] for h in houses])))

# Sort pearson scores by absolute value of score * 1 - p-value
'''
pearson_scores.sort(key=lambda s: abs(s[1] * (1 - s[2])), reverse=True)
pearson_scores = [["=========", "=============", "======="]] + pearson_scores[:]
pearson_scores = [["Attribute", "Pearson Score", "P-value"]] + pearson_scores[:]
for s in pearson_scores:
    padding1 = 20 - len(s[0])
    print(s[0] + " " * padding1, end='')
    padding2 = 20 - len(str(s[1]))
    print(str(s[1]) + " " * padding2, end='')
    print(s[2])
'''