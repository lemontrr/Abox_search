
import os
for filename in os.listdir('./'):
    if 'bit' in filename[:5]:
        with open(filename,'r') as f:
            print(filename+'\t',len(f.readlines()))
