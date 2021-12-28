import csv
import json
import os
import requests
import glob
import copy

files = glob.glob("data/tmp/*.json")

prefix = "https://nakamura196.github.io/E34"

curations = []

for i in range(len(files)):
    
    # for file in files:

    file = files[i]
    print(i+1, len(files), file)

    with open(file) as f:
        map = json.load(f)

    base = os.path.basename(file)

    cn = os.path.splitext(base)[0]

    # print(cn)

    manifest_path = "../docs/iiif/"+cn+"/manifest.json"

    with open(manifest_path) as f:
        manifest = json.load(f)

    canvases = manifest["sequences"][0]["canvases"]

    images = {}

    for canvas in canvases:
        images[canvas["thumbnail"]["service"]["@id"]] = canvas["@id"]

    # print(images)

    members = []
    members2 = []

    chars = {}

    for image in sorted(map):

        if image not in images:
            continue

        canvas = images[image]

        # print(canvas)

        for item in map[image]:

            xywh = item["thumbnail_url"].split(".tif/")[1].split("/")[0]

            member_id = canvas + "#xywh=" + xywh

            char = item["title"].split("@")[0]

            if char == "null":
                continue

            if char not in chars:
                chars[char] = 0

            chars[char] += 1

            id = item["id"]

            code = item["unicode"]

            member = {
                "label": id,
                "metadata": [
                    {
                    "value": [
                        {
                        "motivation": "sc:painting",
                        "@type": "oa:Annotation",
                        "on": member_id,
                        "resource": {
                            "chars": "{}<br/><a href=\"https://hi-ut.github.io/kuzushiji/item/{}/{}\">U+{}</a>".format(char, char, id, code),
                            "format": "text/html",
                            "@type": "cnt:ContentAsText",
                            "marker": {
                                "text": char
                            }
                        },
                        "@id": member_id + "#" + id
                        }
                    ],
                    "label": "Annotation"
                    },
                    {
                        "label": "char",
                        "value" : char
                    },
                    {
                        "label": "call_number",
                        "value" : item["source"]["call_number"].split("@")[0]
                    },
                    {
                        "label": "date",
                        "value" : item["source"]["date"].split("@")[0]
                    },
                    {
                        "label": "date_str",
                        "value" : item["source"]["date_str"].split("@")[0]
                    },
                    {
                        "label": "division",
                        "value" : item["source"]["division"].split("@")[0]
                    },
                    {
                        "label": "document",
                        "value" : item["source"]["document"].split("@")[0]
                    },
                    {
                        "label": "occupation",
                        "value" : item["source"]["occupation"].split("@")[0]
                    },
                    {
                        "label": "send",
                        "value" : item["source"]["send"].split("@")[0]
                    },
                    {
                        "label": "to",
                        "value" : item["source"]["to"].split("@")[0]
                    },
                    {
                        "label": "value",
                        "value" : item["source"]["value"].split("@")[0]
                    }
                ],
                "@type": "sc:Canvas",
                "@id": member_id,
                "thumbnail": item["thumbnail_url"]
            }

            member2 = copy.deepcopy(member) #変更行

            member2["metadata"][0]["value"][0]["resource"]["marker"] = {
                "border-width": 1,
                "border-color": "#e41a1c"
            }

            members.append(member)
            members2.append(member2)

    if len(members) == 0:
        continue

    label = manifest["label"]
    
    curation = {
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://codh.rois.ac.jp/iiif/curation/1/context.json"
        ],
        "@type": "cr:Curation",        
        "@id": prefix + "/curation/" + cn + "/character.json",
        "selections": [
            {
                "members" : members,
                "@type": "sc:Range",
                "within": {
                    "@id": manifest["@id"],
                    "@type": "sc:Manifest",
                    "label": label
                },
                "@id": manifest["@id"]
            }
        ],
        
        "viewingHint": "annotation",
        
        
    }

    path = "../docs/curation/" + cn + "/character.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as outfile:
        json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

    ####

    curation2 = copy.deepcopy(curation) #変更行

    curation2["@id"] = curation2["@id"].replace("character", "box")
    curation2["selections"][0]["members"] = members2

    path = path.replace("character", "box")

    with open(path, 'w') as outfile:
        json.dump(curation2, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

    ####

    count = 0
    for key in chars:
        count += chars[key]

    canvases = []

    aaa = {}

    for member in members:
        canvas = member["@id"].split("#xywh=")[0]
        if canvas not in canvases:
            canvases.append(canvas)

        metadata = member["metadata"]

        for m in metadata:
            if m["label"] != "Annotation":
                label2 = m["label"]
                value = m["value"]

                if label2 not in aaa:
                    aaa[label2] = {}

                if value not in aaa[label2]:
                    aaa[label2][value] = 0

                aaa[label2][value] += 1

    print(aaa)

    curations.append({
        "size" : len(chars.keys()),
        "total" : count,
        "label" : label.split("@")[0],
        "id" : cn,
        "canvas_size" : len(canvases)
    })

path2 = "data/curations.json"
path2 = "../../outougata/static/data/curations.json"

with open(path2, 'w') as outfile:
    json.dump(curations, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))
    