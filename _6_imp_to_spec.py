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

n = 5
MC = 3
L = MC - int((n-1)/2)
op_dc = min([max([2**(n-L),2]),2**n])
lc_bnd = [4,4,4,4,8,8,12,16,24]
op_lc = min([max([2**(n-(MC-n+1))]),2**n])
filename = f'Imp_{n}bit_{MC}MC_{op_dc}dc_{op_lc}lc.txt'
# fix_dc = 64
# fix_lc = 128
# filename = f'Imp_{n}bit_{MC}MC_{fix_dc}dc_{fix_lc}lc.txt'
try:
    with open(filename,'r') as f:
        imp = f.read()
except:
    with open(filename,'w') as f:
        print('make a file',filename)
    import os
    os.system(filename)
    exit()

X_list = [[(i>>j)&1 for j in range(n)] for i in range(2**n)]
S = []
Y = [0]*n
T = [0]*MC
for X in X_list:
    exec(imp)
    out = 0
    for i in range(n):
        out |= Y[i]<<i
    S.append(out)
bij = 'non-bijective'
if len(list(set(S)))==2**n:
    bij = 'bijective'
    
ddt = make_ddt(S,2**n,2**n)
lat = make_lat(S,2**n,2**n)
dc = max([max(i) for i in ddt[1:]])
lc = max([max(i[1:]) for i in lat])
print('')
print(f'{n}bit {MC}MC {dc}dc {lc}lc',bij)
print('')

# print(S)
    