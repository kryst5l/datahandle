#coding:utf-8


import os


def rename_file(path):
    for dirpath,dirnames,filenames in os.walk(path):
        for filename in filenames:
            real_name = os.path.join(dirpath,filename)
            return real_name


if __name__ == '__main__':
    path = '/home/mobvoi/data_collect/CNS/0221/0221_export'
    #real_name = rename_file(path)
    f = open('/home/mobvoi/data_collect/CNS/0221/0221_export/hotword.txt','r')
    new_f = open('/home/mobvoi/data_collect/CNS/0221/0221_export/new.txt','w')
    content = f.read()
    for dirpath,dirnames,filenames in os.walk(path):
        for filename in filenames:
            if filename.split('.')[-1] != 'txt':
                real_name = os.path.join(dirpath,filename)
                print(real_name)
                #此时的real_name : xxxxx_0301to0350_czc_31.wav
		#print(real_name.split('_')[1][1:4])
                modify_name = str(int(filename.split('_')[0][0:4]) + int(filename.split('_')[2].split('.')[0]) - 1) + '.wav'
                modify_name_fin = os.path.join(path,modify_name)
                os.rename(real_name,modify_name_fin)
		print(filename,modify_name)
                content = content.replace(filename,modify_name[:-4])
    new_f.write(content)
    f.close()
    new_f.close()

   # os.system(cmd)
