ren mergedGachaData.json oldGachaData.json
py capture.py -o capturedGachaData.json
py merge.py -i capturedGachaData.json oldGachaData.json -o mergedGachaData.json
py writeXLSX.py -i mergedGachaData.json
pause