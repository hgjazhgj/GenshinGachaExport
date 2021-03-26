import json


def merge(captureData, localData):
    gachaData = {}
    accept = False
    for gachaType in set(gachaData) | set(localData):
        try:
            captureTypeData = captureData.get(gachaType, [])
            localTypeData = localData.get(gachaType, [])
            mergeTypeData = captureTypeData + localTypeData[len(
                localTypeData) - localTypeData[::-1].index(captureTypeData[-1]):]
        except(IndexError, ValueError):
            print(f"merge {gachaType} failed in {len(captureTypeData)} and {len(localTypeData)} record(s)")
            mergeTypeData = captureTypeData + localTypeData
        else:
            print(f"add {len(mergeTypeData)-len(localTypeData)} record(s) to {gachaType}")
            accept = True
        finally:
            gachaData[gachaType] = mergeTypeData
    assert accept
    return gachaData


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, nargs=2)
    parser.add_argument("-o", type=str, default="mergedGachaData.json")
    args = parser.parse_args()
    with open(args.i[0], "r", encoding="utf-8") as f:
        data1 = json.load(f)
    with open(args.i[1], "r", encoding="utf-8") as f:
        data2 = json.load(f)
    data = merge(data1, data2)
    with open(args.o, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=False, indent=4)
