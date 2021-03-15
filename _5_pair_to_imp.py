def make_ddt(S,n,m):
    ddt = [[0 for i in range(m)]for j in range(n)]
    for i in range(n):
        for j in range(n):
            ddt[i^j][S[i]^S[j]] += 1
    return ddt

def make_lat(S,n,m):
    lat = [[n for i in range(m)]for j in range(n)]
    for i in range(n):
        for j in range(m):
            for x in range(n):
                lat[i][j] -= bin((x&i)^(S[x]&j)).count('1')%2
                lat[i][j] -= bin((x&i)^(S[x]&j)).count('1')%2
    return lat

def selected_to_Abox(pair,n):
    MC = int(len(pair)/2)
    AND_Gate = [[pair[2*i],pair[2*i+1]] for i in range(MC)]
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
    return S

def selected_to_imp(pair,n,filename):
    MC = int(len(pair)/2)
    AND_Gate = [[pair[2*i],pair[2*i+1]] for i in range(MC)]
    text = ''
    for i in range(MC):
        line_text = f'T[{i}] = '
        line_text += '('
        for j in range(n):
            if AND_Gate[i][0]&(1<<j) != 0:
                line_text += f'^X[{j}]'
        for j in range(i):
            if AND_Gate[i][0]&(1<<(n+j)) != 0:
                line_text += f'^T[{j}]'
        line_text += ')&('
        for j in range(n):
            if AND_Gate[i][1]&(1<<j) != 0:
                line_text += f'^X[{j}]'
        for j in range(i):
            if AND_Gate[i][1]&(1<<(n+j)) != 0:
                line_text += f'^T[{j}]'
        line_text += ')\n'
        text += line_text
    with open(filename,'w') as f:
        f.write(text)
        
Abox_63 = [1, 2, 4, 8, 16, 32]
Abox_64 = [1, 2, 4, 8, 16, 32, 21, 42]
Abox_65 = [1, 2, 4, 8, 16, 32, 21, 42, 27, 45]
Abox_74 = [1, 2, 1, 4, 8, 16, 32, 64]
Abox_75 = [1, 2, 1, 4, 8, 16, 32, 64, 42, 84]
Abox_76 = [1, 2, 1, 4, 8, 16, 32, 64, 42, 84, 54, 91]
Abox_84 = [1, 2, 4, 8, 16, 32, 64, 128]
Abox_85 = [1, 2, 4, 8, 16, 32, 64, 128, 85, 170]
test = [1, 2, 1, 4, 8, 16, 32, 64, 383, 78]
test = [1, 2, 1, 4, 8, 16, 32, 64, 306, 383]

pair = test
n = 7
MC = 5

Abox = selected_to_Abox(pair,n)
ddt = make_ddt(Abox,2**n,2**MC)
lat = make_lat(Abox,2**n,2**MC)
dc = max([max(i) for i in ddt[1:]])
lc = max([max(i) for i in lat[1:]])
print(pair,dc,lc)
exit()
filename = f'Imp_{n}bit_{MC}AND_{dc}dc_{lc}lc.txt'
selected_to_imp(pair,n,filename)
print(Abox)
print('create',filename)
import os
os.system(filename)