import json

def convert(olddata):
    gachatype = {
        i["key"]:i["name"]
        for i in olddata["gachaType"]
    }
    return {
        gachatype[i]:[
            {
                "time": k["time"],
                "name": k["name"],
                "type": k["item_type"],
                "rank": int(k["rank_type"]),
            }
            for k in j
        ]
        for i,j in olddata["gachaLog"].items()
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str)
    parser.add_argument("-o", type=str, default="convertedGachaData.json")
    args = parser.parse_args()
    with open(args.i, "r", encoding="utf-8") as f:
        olddata = json.load(f)
    newdata = convert(olddata)
    with open(args.o, "w", encoding="utf-8") as f:
        json.dump(newdata, f, ensure_ascii=False, sort_keys=False, indent=4)
