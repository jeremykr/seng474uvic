import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.interpolate import spline
from scipy.stats import pearsonr
from utils import Utils

#houses = Utils.get_house_data("../RemaxScrape/remaxVanDataset.json", "Vancouver")
houses = Utils.get_house_data("../RemaxScrape/remaxDataset2.json", "Victoria")

houses.sort(key=lambda h: h.price, reverse=True)

prices = [h.price for h in houses]
spaces = [h.square_footage for h in houses]
bedrooms = [h.bedrooms for h in houses]
bathrooms = [h.bathrooms for h in houses]
landSizes = [h.land_size for h in houses]
walkScores = [h.walk_score for h in houses]
avgLocalPrices = [h.average_local_price for h in houses]
random = [np.random.random() for _ in houses]

attributes = {"price" : prices, "space" : spaces, "bedrooms": bedrooms, \
                "bathrooms": bathrooms, "land size": landSizes, "random": random, \
                "walk score": walkScores, "avg local price": avgLocalPrices}

pearson_scores = {}
for key in attributes:
    pearson_scores[key] = pearsonr(attributes["price"], attributes[key])

pearson_scores = [(k, pearson_scores[k]) for k in pearson_scores]
pearson_scores.sort(key=lambda t: abs(t[1][0] * (1 - t[1][1])), reverse=True)

spacing = 20

for s in pearson_scores:
    attrib = s[0]
    score = str(s[1][0])
    pval = str(s[1][1])
    print(attrib + " " * (spacing - len(attrib)), end="")
    print(score + " " * (spacing - len(score)), end="")
    print(pval + " " * (spacing - len(pval)))