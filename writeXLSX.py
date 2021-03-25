import json
import xlsxwriter

def writeXLSX(gachaData, filename):
    workbook = xlsxwriter.Workbook(filename)
    content_css = workbook.add_format({"align": "left", "font_name": "微软雅黑", "border_color": "#c4c2bf","bg_color": "#ebebeb", "border": 1})
    title_css = workbook.add_format({"align": "left", "font_name": "微软雅黑", "color": "#757575", "bg_color": "#dbd7d3", "border_color": "#c4c2bf", "border": 1, "bold": True})
    star_5 = workbook.add_format({"color": "#bd6932", "bold": True})
    star_4 = workbook.add_format({"color": "#a256e1", "bold": True})
    star_3 = workbook.add_format({"color": "#8e8e8e"})
    for id in gachaData:
        gachaDictList = gachaData[id][::-1]
        worksheet = workbook.add_worksheet(id)
        excel_col = ["A", "B", "C", "D", "E", "F"]
        excel_header = ['时间', '名称', '类别', '星级', '总次数', '保底内']
        worksheet.set_column("A:A", 22)
        worksheet.set_column("B:B", 14)
        for i in range(len(excel_col)):
            worksheet.write(f"{excel_col[i]}1", excel_header[i], title_css)
        worksheet.freeze_panes(1, 0)
        idx = 0
        pdx = 0
        i=2
        for gacha in gachaDictList:
            idx = idx + 1
            pdx = pdx + 1
            excel_data = [gacha["time"], gacha["name"], gacha["type"], gacha["rank"], idx, pdx]
            for j in range(len(excel_col)):
                worksheet.write(f"{excel_col[j]}{i}", excel_data[j], content_css)
            if excel_data[3] == 5:
                pdx = 0
            i+=1
        worksheet.conditional_format(f"A2:F{len(gachaDictList)+1}", {"type": "formula", "criteria": "=$D2=5", "format": star_5})
        worksheet.conditional_format(f"A2:F{len(gachaDictList)+1}", {"type": "formula", "criteria": "=$D2=4", "format": star_4})
        worksheet.conditional_format(f"A2:F{len(gachaDictList)+1}", {"type": "formula", "criteria": "=$D2=3", "format": star_3})
    workbook.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="genshin-gacha-export")
    parser.add_argument("-i", type=str)
    parser.add_argument("-o", type=str, default="gachaExport.xlsx")
    args = parser.parse_args()
    with open(args.i, "r", encoding="utf-8") as f:
        data = json.load(f)
    writeXLSX(data, args.o)
