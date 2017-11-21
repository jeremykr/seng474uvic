import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.interpolate import spline
from scipy.stats import pearsonr


data = []

with open("RemaxScrape/remaxVanDataset.json") as f:
    data = json.load(f)

houses = []
attribs = ['price', 'bathrooms', 'bedrooms', \
            'landSize', 'rooms', 'space', 'ageofBuilding', \
            'daysonMarket', 'walkScore', 'transitScore', 'averageLocalPrice']

def filter_attributes(A, listing):
    for a in A:


for d in data:
    try:
        attrib_missing = False
        attrib_values = []
        for a in attribs:
            x = -1
            if a == "averageLocalPrice":
                if d[a][-1] == "k":
                    x = int(d[a][1:-1]) * 1000
                else:
                    x = int(d[a][1:])
            elif d[a] != "": 
                x = int(d[a])
            if x == -1:
                attrib_missing = True
                break
            else:
                attrib_values.append(x)
        if attrib_missing: continue

        house_attribs = [x for x in attrib_values]
        houses.append(house_attribs + [np.random.random()])

    except e: print(e)

attribs.append("random")

X = range(len(houses))
houses.sort(key=lambda h: h[0])
prices = [h[0] for h in houses]
print(prices)
print("Houses: ", len(prices), end="\n\n")
pearson_scores = []
for i in range(len(houses[0])):
    pearson_scores.append([attribs[i]] + list(pearsonr(prices, [h[i] for h in houses])))

# Sort pearson scores by absolute value of score * 1 - p-value
pearson_scores.sort(key=lambda s: abs(s[1] * (1 - s[2])), reverse=True)
pearson_scores = [["=========", "=============", "======="]] + pearson_scores[:]
pearson_scores = [["Attribute", "Pearson Score", "P-value"]] + pearson_scores[:]
for s in pearson_scores:
    padding1 = 20 - len(s[0])
    print(s[0] + " " * padding1, end='')
    padding2 = 20 - len(str(s[1]))
    print(str(s[1]) + " " * padding2, end='')
    print(s[2])