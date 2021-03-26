import json
import os
import re
import urllib.parse
import requests

URL_GACHATYPE = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getConfigList"
URL_GACHALOG = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog"


def getGachaLogs(gachaTypeId, query):
    def gen():
        page = 1
        end_id = "0"
        while True:
            print(f"fetching gachaType {gachaTypeId} page {page}")
            data = requests.get(URL_GACHALOG + "?" + urllib.parse.urlencode(dict(query, **{
                "size": "20",
                "gacha_type": gachaTypeId,
                "page": page,
                "lang": "zh-cn",
                "end_id": end_id,
            }))).json()["data"]["list"]
            if not data:
                break
            yield from ({
                "time": record["time"],
                "name": record["name"],
                "type": record["item_type"],
                "rank": int(record["rank_type"]),
            }for record in data)
            page += 1
            end_id = data[-1]["id"]
    return list(gen())


def capture():
    with open(os.path.join(os.environ["USERPROFILE"], "AppData", "LocalLow", "miHoYo", "原神", "output_log.txt"), "r") as f:
        query = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(
            re.search("OnGetWebViewPageFinish:.*(\\?.*#/log)", f.read()).group(1)).query))
    return {j: getGachaLogs(i, query)
            for i, j in (
                (i["key"], i["name"])
                for i in
        requests.get(URL_GACHATYPE + "?" +
                     urllib.parse.urlencode(dict(query, lang="zh-cn")))
        .json()["data"]["gacha_type_list"]
    )
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", type=str, default="gachaData.json")
    args = parser.parse_args()
    with open(args.o, "w", encoding="utf-8") as f:
        json.dump(capture(), f, ensure_ascii=False, sort_keys=False, indent=4)
