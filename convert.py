def convert(olddata):
    gachatype = {
        i["key"]: i["name"]
        for i in olddata["gachaType"]
    }
    return {
        gachatype[i]: [
            {
                "time": k["time"],
                "name": k["name"],
                "type": k["item_type"],
                "rank": int(k["rank_type"]),
            }for k in j
        ]for i, j in olddata["gachaLog"].items()
    }
