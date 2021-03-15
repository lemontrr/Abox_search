import ksbox
import re
import random
filename = '8bit_12AND_10dc.txt'
n = int(re.findall("\d+",filename)[0])
MC = int(re.findall("\d+",filename)[1])
min_dc = 999
min_lc = 999

AND_list = []
with open(filename,'r') as f:
    lines = f.readlines()
lenth = len(lines)
for line in lines:
    ANDs = list(map(int,line.split(' ')[:-1]))
    AND_list.append(ANDs)
num = 0
for AND_c in AND_list:
    num += 1
    AND_Gate = [[AND_c[2*i],AND_c[2*i+1]] for i in range(MC)]

    output = [0]*MC
    A_box = []
    for x in range(2**n):
        val = x
        for i in range(MC):
            output[i] = (bin(val&AND_Gate[i][0]).count('1')%2) & (bin(val&AND_Gate[i][1]).count('1')%2)
            val |= output[i]<<(i+n)
        out = 0
        for i in range(MC):
            out |= output[i]<<i
        A_box.append(out)
    
    A_per = []
    A_inv_per = []
    A = [0]*100
    for A[0] in range(MC):
        for A[1] in range(A[0]+1,MC):
            for A[2] in range(A[1]+1,MC):
                for A[3] in range(A[2]+1,MC):
                    for A[4] in range(A[3]+1,MC):
                        for A[5] in range(A[4]+1,MC):
                            for A[6] in range(A[5]+1,MC):
                                for A[7] in range(A[6]+1,MC):
                                    A_per.append(tuple(A))
                                    A_inv_per.append(tuple([i for i in range(MC) if i not in A]))
    A_box_bin = []
    for x in range(2**n):
        A_box_bin.append(list(map(int,list(bin(A_box[x])[2:].zfill(MC)))))
    for number in range(len(A_per)):
        for rands in range(100):
            A = [random.randrange(0,n) for i in range(MC-n)]
            S_box = []
            for x in range(2**n):
                y = 0 
                for i in range(n):
                    y <<= 1
                    y |= A_box_bin[x][A_per[number][i]]
                for i in range(MC-n):
                    y ^= A_box_bin[x][A_inv_per[number][i]]<<A[i]
                S_box.append(y)
            ddt = ksbox.make_ddt(S_box)
            lat = ksbox.make_lat(S_box)
            dc = ksbox.table_max(ddt)
            lc = ksbox.table_max(lat)
            if min_dc>dc:
                min_dc = dc
                with open(f'{n}bit_{MC}MC_{dc}dc_{lc}lc.txt','w') as f:
                    f.write(f'{AND_c} {A_per[number]} {A_inv_per[number]} {A}\n')
            if min_lc>lc:
                min_lc = lc
                with open(f'{n}bit_{MC}MC_{dc}dc_{lc}lc.txt','w') as f:
                    f.write(f'{AND_c} {A_per[number]} {A_inv_per[number]} {A}\n')
            print(dc,lc,f' vs  {min_dc} {min_lc}    // {rands}-{number}/{len(A_per)}-{num}/{len(AND_c)}')



