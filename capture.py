import os
import re
from urllib import parse
import requests

URL_GACHATYPE = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getConfigList"
URL_GACHALOG = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog"


def getGachaLogs(gachaTypeId, query):
    def gen():
        page = 1
        endId = "0"
        while True:
            print(f"fetching gachaType {gachaTypeId} page {page}")
            data = requests.get(URL_GACHALOG + "?" + parse.urlencode(dict(query, **{
                "size": "20",
                "gacha_type": gachaTypeId,
                "page": page,
                "lang": "zh-cn",
                "end_id": endId,
            }))).json()["data"]["list"]
            yield from ({
                "time": record["time"],
                "name": record["name"],
                "type": record["item_type"],
                "rank": int(record["rank_type"]),
            }for record in data)
            if len(data)<20:
                break
            page += 1
            endId = data[-1]["id"]
    return list(gen())


def capture():
    with open(os.path.join(os.environ["USERPROFILE"], "AppData", "LocalLow", "miHoYo", "原神", "output_log.txt"), "r") as f:
        query = dict(parse.parse_qsl(parse.urlparse(
            re.search("OnGetWebViewPageFinish:.*(\\?.*#/log)", f.read()).group(1)).query))
    return {
        i["name"]: getGachaLogs(i["key"], query)
        for i in requests.get(
            URL_GACHATYPE + "?" + parse.urlencode(dict(query, lang="zh-cn"))
        ).json()["data"]["gacha_type_list"]
    }
