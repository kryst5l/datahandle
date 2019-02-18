# -*- coding:utf-8 -*-
import openpyxl
from pydub import AudioSegment
import os

def slice_audio_by_pydub():
    wb = openpyxl.load_workbook('points.xlsx')
    sheet = wb.get_active_sheet()
    start_num = 0
    count = 0
    if not os.path.exists(audio_path + '/slices'):
        os.makedirs(audio_path + '/slices')

    for row in list(sheet.iter_rows())[1:]:
        count += 1
        input_path = audio_path + '/' + row[0].value
        slices = row[1].value.split(';')
        slices.pop(-1)
        print(count, "点位：", slices)
        for index, s in enumerate(slices):
            start_num += 1
            out_path = audio_path + '/slices/' + str(start_num).zfill(6) + '.mp3'
            start_time = float(s.split(',')[0]) * 1000
            end_time = float(s.split(',')[1]) * 1000
            print("start:", start_time)
            print("end:", end_time)
            sound = AudioSegment.from_mp3(input_path)
            word = sound[start_time:end_time]
            word.export(out_path, format="wav")
            print(index + 1, ":  ", out_path, "生成成功")

def main():
    slice_audio_by_pydub()

if __name__ == "__main__":
    excel_path = input("日期(例20190101):")
    audio_path = input("音频源文件夹:")
    main()
    print("Finish")