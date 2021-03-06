import csv
import json

items = []

res = {
    "pos" : 0,
    "neg" : 0
}

metadata = {}

with open('data/TBL_M_E34_list.txt', encoding='utf-8', newline='') as f:
    for cols in csv.reader(f, delimiter='\t'):

        for k in range(len(cols)):
            value = cols[k]
            if k not in metadata:
                metadata[k] = {}

            if value not in metadata[k]:
                metadata[k][value] = 0
            
            metadata[k][value] += 1
        

        id = cols[0]

        date_str = cols[6]
        date = cols[7]

        send = cols[27] + "@ja" if cols[27] != "null" else ""
        to = cols[28] + "@ja" if cols[28] != "null" else ""

        occupation = cols[29].replace("|", ",")  + "@ja" if cols[29] != "null" else ""

        document = cols[25] + "@ja"
        value = cols[26] + "@ja"

        char = cols[17]
        doc = cols[26]

        unicode = cols[22] if cols[22] != "null" else ""

        img11 = cols[38] 
        img10 = cols[59] # 000
        img0 = cols[61] if cols[61] != "null" else ""
        img1 = cols[62] if cols[62] != "null" else ""
        img2 = cols[64] if cols[64] != "null" else ""
        img3 = cols[70] if cols[70] != "null" else ""
        img4 = ".tif" # cols[71] # .tif

        cn = img0 + "-" + img1 + "-" + img2

        # print(cn)

        x = cols[32]
        y = cols[33]
        
        
        if x != "null":

            res["pos"] +=1
        
            w = int(cols[34]) - int(x)
            h = int(cols[35]) - int(y)

            url = "https://clioimg.hi.u-tokyo.ac.jp/viewer/image/{}/{}/{}/{}/{}/{}{}".format(img11, img10, img0, img1, img2, img3, img4)

            api = "https://clioimg.hi.u-tokyo.ac.jp/viewer/api/image/{}/{}/{}/{}/{}/{}{}".format(img11, img10, img0, img1, img2, img3, img4)

            thumbnail = api + "/{},{},{},{}/200,/0/default.jpg".format(x, y, w, h)

            # print(url, thumbnail)

            # print(id, char, doc)

            source = {
                "call_number": "{}@ja".format(cn),
                "date": date,
                "date_str" : date_str,
                "division": "XX@ja",
                "document": document,
                "occupation": occupation,
                # "page": "00000052",
                # "remarks": "",
                "send": send,
                "to": to,
                "value": value
            }
                

            item = {
                "creator" : "???????????????????????????@ja",
                "delegate" : 0,
                "id" : id,
                "identifier" : "https://clioapi.hi.u-tokyo.ac.jp/shipsapi/v1/W34/controlnumber/" + id,
                "manifest_url" : "",
                "rights" : "",
                "rights_url": "https://www.hi.u-tokyo.ac.jp/faq/reuse_cc-by.html",
                "source": source,
                "subject": "????????????????????????@ja",
                "thumbnail_url": thumbnail,
                "title": "{}@ja".format(char),
                "unicode": unicode
            }

            items.append(item)

            # break

        else:
            res["neg"] +=1

'''
with open("data/items.json", 'w') as outfile:
    json.dump(items, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))
'''

print(res)

with open("data/metadata.json", 'w') as outfile:
    json.dump(metadata, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))

freq = {}

for i in metadata:

    obj = metadata[i]

    score_sorted = sorted(obj.items(), key=lambda x:x[1], reverse=True)

    freq[i] = {
        "count": len(obj),
        "list" : score_sorted[0:10]
    }

with open("data/freq.json", 'w') as outfile:
    json.dump(freq, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))