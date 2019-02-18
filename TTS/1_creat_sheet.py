# -*- coding:utf-8 -*-

import os
from _decimal import Decimal
import textgrid
import xlsxwriter
'''

根据音频对应textgrid生成对应的断点excel
音频格式应为wav

'''
def read_textgrid(path):
    tg = textgrid.TextGrid()
    tg.read(path)
    return tg

def main():
    count = 0
    text = ''
    wb = xlsxwriter.Workbook('points.xlsx')
    ws = wb.add_worksheet("Sheet1")
    ws.write("A1", "名称")
    ws.write("B1", "标注点")
    for file in os.listdir(text_path):
        points = []
        if file.endswith('.TextGrid'):
            try:
                print(file)
                name = file[:-9] + '.mp3'
                info = read_textgrid(os.path.join(text_path, file))
                item_one = info.tiers[0]
                for index in range(0, len(item_one)):
                    points.append(item_one[index].minTime.quantize(Decimal('0.0000')))
                    points.append(',')
                    points.append(item_one[index].maxTime.quantize(Decimal('0.0000')))
                    points.append(';')
                ws.write(count + 1, 0, name)
                for point in points:
                    text += str(point)
                print(text)
            except textgrid.exceptions.TextGridError:
                with open('errors.txt', 'a') as f:
                    f.write(file + '\n')
                text = ''
                print("read textgrid error")
            ws.write(count + 1, 1, text)
            text = ''
            count += 1
    wb.close()

if __name__ == '__main__':
    text_path = input("输入文本路径：")
    main()
