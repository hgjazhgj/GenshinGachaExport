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
