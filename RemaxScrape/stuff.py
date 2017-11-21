import json

data = []
with open("remaxDataset2.json") as f:
    data = json.load(f)

pcode_prefixes = {}
for d in data:
    try:
        pc_prefix = d['address']['postal'][:3]
        if pc_prefix not in pcode_prefixes:
            pcode_prefixes[pc_prefix] = 1
        else:
            pcode_prefixes[pc_prefix] += 1
    except:
        pass

print(len(pcode_prefixes.keys()))
pcode_prefixes = map(lambda p: hash(p) % 10000, pcode_prefixes)
print(list(pcode_prefixes))