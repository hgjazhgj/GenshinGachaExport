import json

def merge(captureData, localData):
    gachaData = {}
    for gachaType in captureData:
        gachaTypeData = captureData[gachaType]
        try:
            gachaTypeData += localData[gachaType][localData[gachaType].index(gachaTypeData[-1])+1:]
        except IndexError:
            gachaTypeData = localData[gachaType]
        except ValueError:
            assert not localData[gachaType]
        except KeyError:
            pass
        gachaData[gachaType]=gachaTypeData
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
