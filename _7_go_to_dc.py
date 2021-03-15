import os.path
import re

path_dir = os.getcwd()
list_dir = os.listdir(path_dir)
for filename in list_dir:
    if 'under' in filename:
        with open(filename,'r') as f:
            lines = f.readlines()
        MC = re.findall("\d+",filename)[1]
        for line in lines:
            numbers = re.findall("\d+",line)
            with open(f'8bit_{MC}AND_{numbers[-1]}dc.txt','a') as f:
                data = ''
                for i in numbers[:-1]:
                    data += f'{i} '
                data += '\n'
                f.write(data)