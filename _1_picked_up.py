
import os
for n in range(3,9):
    MC = int((n-1)/2)+1
    filename = f"{n}bit_{MC}AND__init.txt"
    AND_list=[]
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            ANDs = list(map(int,line.split(' ')[:-1]))
            AND_list.append(ANDs)
    NEW_AND = []
    for AND_c in AND_list:
        AND_Gate = [[AND_c[2*i],AND_c[2*i+1]] for i in range(MC)]
        output = [0]*MC
        S = []
        for x in range(2**n):
            val = x
            for i in range(MC):
                output[i] = (bin(val&AND_Gate[i][0]).count('1')%2) & (bin(val&AND_Gate[i][1]).count('1')%2)
                val |= output[i]<<(i+n)
            out = 0
            for i in range(MC):
                out |= output[i]<<i
            S.append(out)
        ddt = [[0 for j in range(2**MC)] for i in range(2**n)]
        for i in range(2**n):
            for j in range(i+1,2**n):
                ddt[i^j][S[i]^S[j]] += 2
        dc = max([max(i) for i in ddt[1:]])
        if dc == 2**(n-1):
            NEW_AND.append(AND_c)
    with open(f"{n}bit_{MC}AND_{2**(n-1)}dc.txt",'w') as f:
        pass
    with open(f"{n}bit_{MC}AND_{2**(n-1)}dc.txt",'a') as f:
        for i in NEW_AND:
            text = ''
            for j in i:
                text += f'{j} '
            text += '\n'
            f.write(text)