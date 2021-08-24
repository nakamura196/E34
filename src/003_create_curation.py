import csv
import json
import os
import requests
import glob
import copy

files = glob.glob("data/tmp/*.json")

prefix = "https://nakamura196.github.io/E34"

for file in files:

    with open(file) as f:
        map = json.load(f)

    base = os.path.basename(file)

    cn = os.path.splitext(base)[0]

    print(cn)

    manifest_path = "../docs/iiif/"+cn+"/manifest.json"

    with open(manifest_path) as f:
        manifest = json.load(f)

    canvases = manifest["sequences"][0]["canvases"]

    images = {}

    for canvas in canvases:
        images[canvas["thumbnail"]["service"]["@id"]] = canvas["@id"]

    print(images)

    members = []
    members2 = []

    for image in sorted(map):

        if image not in images:
            continue

        canvas = images[image]

        print(canvas)

        for item in map[image]:

            xywh = item["thumbnail_url"].split(".tif/")[1].split("/")[0]

            member_id = canvas + "#xywh=" + xywh

            char = item["title"].split("@")[0]

            if char == "null":
                continue

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
                    }
                ],
                "@type": "sc:Canvas",
                "@id": member_id
            }

            member2 = copy.deepcopy(member) #変更行

            del member2["metadata"][0]["value"][0]["resource"]["marker"]

            members.append(member)
            members2.append(member2)

    if len(members) == 0:
        continue
    
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
                    "label": manifest["label"]
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


    