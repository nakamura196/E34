import csv
import json
import os
import requests

map = {}

with open("data/items.json") as f:
    items = json.load(f)

    for item in items:
        source = item["source"]

        cn = source["call_number"].replace("@ja", "")

        if cn not in map:

            map[cn] = {}

        api = item["thumbnail_url"].split(".tif/")[0] + ".tif"
        
        tmp = map[cn]

        if api not in tmp:
            tmp[api] = []

        tmp[api].append(item)

print(len(map.keys()))

prefix = "https://nakamura196.github.io/E34"

for cn in map:
    path = "../docs/iiif/" + cn + "/manifest.json"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    canvases = []

    data = map[cn]

    index = 0

    init = True

    metadata = []
        
    for api in sorted(data):

        if init:
            item = data[api][0]

            source = item["source"]

            label = source["value"]

            for key in source:
                metadata.append({
                    "label" : key,
                    "value" : source[key]
                })

        init = False

        index += 1

        info = api + "/info.json"

        image_path = api.replace("https://clioimg.hi.u-tokyo.ac.jp/viewer/api/image", "data/api") + "/info.json"

        if not os.path.exists(image_path):
            df = requests.get(info).json()
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            with open(image_path, 'w') as outfile:
                json.dump(df, outfile, ensure_ascii=False,
                    indent=4, sort_keys=True, separators=(',', ': '))

        with open(image_path) as f:
            image = json.load(f)

        # print(image)

        try:

            w = image["width"]
            h = image["height"]

            canvas = {
                "@id": prefix + "/iiif/"+cn+"/canvas/p{}".format(index),
                "@type": "sc:Canvas",
                "label": "[{}]".format(index),
                "thumbnail": {
                    "@id": api + "/full/200,200/0/default.jpg",
                    "service": {
                    "@context": "http://iiif.io/api/image/2/context.json",
                    "@id": api,
                    "profile": "http://iiif.io/api/image/2/level2.json"
                    }
                },
                "width": w,
                "height": h,
                "images": [
                    {
                        "@id": prefix + "/iiif/"+cn+"/annotation/p{}-image".format(str(index).zfill(4)),
                        "@type": "oa:Annotation",
                        "motivation": "sc:painting",
                        "resource": {
                            "@id": api + "/full/full/0/default.jpg",
                            "@type": "dctypes:Image",
                            "format": "image/jpeg",
                            "width": w,
                            "height": h,
                            "service": {
                            "@context": "http://iiif.io/api/image/2/context.json",
                            "@id": api,
                            "profile": "http://iiif.io/api/image/2/level2.json",
                            "width": w,
                            "height": h
                            }
                        },
                        "on": prefix + "/iiif/"+cn+"/canvas/p{}".format(index)
                    }
                ]
            }
            canvases.append(canvas)

        except Exception as e:
            print(info)
            print(e)

    

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": prefix + "/iiif/" + cn + "/manifest.json",
        "@type": "sc:Manifest",
        "label": label,
        "metadata": metadata,
        "viewingHint": "non-paged",
        "license": "https://www.hi.u-tokyo.ac.jp/faq/reuse_cc-by.html",
        "attribution": "東京大学史料編纂所",
        "logo": "https://www.hi.u-tokyo.ac.jp/common/images/logo.jpg",
        "within": "https://wwwap.hi.u-tokyo.ac.jp/ships/",
        "sequences": [
            {
                "@id": prefix + "/iiif/" + cn + "/sequence/normal",
                "@type": "sc:Sequence",
                "canvases": canvases
            }
        ]
    }

    with open(path, 'w') as outfile:
        json.dump(manifest, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

    with open("data/tmp/" + cn + ".json", 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))