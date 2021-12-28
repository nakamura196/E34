import csv
import json

import glob

files = glob.glob("../docs/curation/*/box.json")

index = []

for i in range(len(files)):
    file = files[i]

    print(i+1, len(files), file)

    with open(file) as f:
        df = json.load(f)

    selection = df["selections"][0]

    for member in selection["members"]:

        metadata = member["metadata"]

        title = ""

        item = {
            "_id" : member["label"],
            # "title" : member
            "thumbnail": member["thumbnail"],
            "manifest": selection["within"]["@id"],
            "member": member["@id"]
        }

        index.append(item)

        for m in metadata:
            label = m["label"]
            value = m["value"]

            if label != "Annotation":
                if label == "char":
                    item["title"] = value
                else:
                    item[label] = value

print("サイズ", len(index))

with open("data/index.json", 'w') as outfile:
    json.dump(index, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))