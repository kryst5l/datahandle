#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
from pydub.audio_segment import AudioSegment
from pydub.silence import detect_nonsilent, detect_silence
from openpyxl import Workbook


#切分音频
def spilt_sound(sound, dbfs, min_silence_len=300, seek_step=10, abadon_len=180):
    count, avg_len, new_range = 0, 0., list()
    print dbfs
    while True:
        the_range = detect_nonsilent(sound, min_silence_len, dbfs, seek_step)
        if the_range:
            max_point = max(the_range, key=lambda x: x[1]-x[0])
            if max_point[1] - max_point[0] < 6000:
                break
        if count > 5:
            break
        count += 1
        dbfs += 3
    count = 1.
    for point in the_range:
        if point[1] - point[0] > abadon_len:
            avg_len += point[1] - point[0]
            count += 1
            new_range.append(point)
    return new_range, avg_len / count

#dbfs=sound.dBFS - 16
#如果min_silence_len定义的太大的话会出现很长的片段
#为了减少切分错误的情况，将其设置的足够小
#期望只出现太短的片段这一种错误情况

def check_range(sound, the_range, avg_len, min_len=600):
    count, add_list, new_range = 0, list(), list()
    for index, point in enumerate(the_range):
        if point[1] - point[0] < max(avg_len-300, min_len) or len(add_list):  #拼接短片段
            add_list.append(point)
            if len(add_list) == 2:
                if add_list[1][0] - add_list[0][1] > 750:
                    new_range.append(add_list[0])
                    new_range.append(add_list[1])
                else:
                    new_range.append([add_list[0][0], add_list[-1][1]])
                add_list=[]
            continue
        new_range.append(point)
    if add_list:
        new_range.append([add_list[0][0], add_list[-1][1]])
    return new_range


if __name__ == '__main__':
    dir_path = raw_input('源文件路径:')
    name_path, str1, error_file = os.listdir(dir_path), '', ''
    wb = Workbook()
    sheet = wb.active
    sheet.title = 'mySheet'
    sheet.append(['文件名', '区域'])
    for index, name in enumerate(name_path):
        if not name.lower().endswith('.wav'):
            continue
        try:
            sound = AudioSegment.from_wav(dir_path+'/'+name).split_to_mono()[0].remove_dc_offset()
            # dbfs = sound.dBFS - 16
            # if dbfs < -60:
            #     dbfs = -60
            dbfs = sound.dBFS - 36
            if dbfs < -66:
                dbfs = -66
            the_range, avg_len = spilt_sound(sound, dbfs, min_silence_len=650)
            new_range = check_range(sound, the_range, avg_len)
            if not os.path.exists(dir_path+'collec'):
                os.mkdir(dir_path+'collec')
            sound.export(dir_path+'collec/'+name, format='wav')
            print '\033[1;32m{}--{}\033[0m'.format(name, 'OK!')
        except:
            error_file += name + '\n'
        for point in new_range: str1 += r'{},{};'.format(point[0]/1000.0, point[1]/1000.0)
        sheet.append([name, str1])
        str1 = ''
    print '\033[1;31m{}:\n{}\033[0m'.format('请检查以下音频文件!!!', error_file)
    wb.save(dir_path+'collec/data.xlsx')
