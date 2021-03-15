import os
import time
import sys

def Alg_one(n,MC):
    L = MC - int((n-1)/2)
    if L <= 1:
        print('Please execute init and picked.')
        return
    dc_cut = max(2**(n-L),2)
    filename = f'{n}bit_{MC}AND_{dc_cut}dc.txt'

    bef_L = L-1
    bef_dc_cut = max(2**(n-bef_L),2)
    if f'{n}bit_{MC-1}AND_{bef_dc_cut}dc.txt' not in os.listdir('./'):
        Alg_one(n,MC-1)
        return
        
    AND_list = []
    with open(f'{n}bit_{MC-1}AND_{bef_dc_cut}dc.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            ANDs = list(map(int,line.split(' ')[:-1]))
            AND_list.append(ANDs)
    len_AND_list = len(AND_list)
    num = 0
    cnt = 0
    min_dc = 999
    st = time.time()
    for num in range(len(AND_list)):
        AND_c = AND_list[num]
        AND_Gate = [[AND_c[2*i],AND_c[2*i+1]] for i in range(MC-1)]
        AND_Gate.append([0,0])
        output = [0]*MC
        S_bef = []
        for x in range(2**n):
            val = x
            for i in range(MC-1):
                output[i] = (bin(val&AND_Gate[i][0]).count('1')%2) & (bin(val&AND_Gate[i][1]).count('1')%2)
                val |= output[i]<<(i+n)
            out = 0
            for i in range(MC-1):
                out |= output[i]<<i
            S_bef.append(out)
            
        S_test = [(S_bef[x]<<n)|x for x in range(2**n)]
        for AND_Gate[MC-1][0] in range(2**(n+MC-1)):
            for AND_Gate[MC-1][1] in range(2**(n+MC-1)):
                if AND_Gate[MC-1][1]<AND_Gate[MC-1][0]: continue
                S = S_bef[:]
                for x in range(2**n):
                    S[x] |= ((bin(S_test[x]&AND_Gate[MC-1][0]).count('1')%2) & (bin(S_test[x]&AND_Gate[MC-1][1]).count('1')%2))<<(MC-1)

                ddt = [[0 for j in range(2**MC)] for i in range(2**n)]
                for i in range(2**n):
                    for j in range(i+1,2**n):
                        ddt[i^j][S[i]^S[j]] += 2
                dc = max([max(i) for i in ddt[1:]])
                if min_dc > dc:
                    min_dc = dc
                if dc == dc_cut:
                    cnt += 1
                    with open(filename,'a') as f:
                        text = ''
                        for i in range(MC):
                            text += f'{AND_Gate[i][0]} {AND_Gate[i][1]} '
                        f.write(text + '\n')
            exe_time = (time.time()-st)/(AND_Gate[MC-1][0]+1)*(2**(n+MC-1))
            print(f'{n}bit {MC}ANDs',f'{num}/{len_AND_list}, {AND_Gate[MC-1][0]}/{(2**(n+MC-1))}, {dc_cut}-{min_dc}, {cnt}' , '%.2f'%(time.time()-st),'%.2f'%exe_time,filename)
        # exe_time = time.time()-st
        # print(f'{n}bit {MC}ANDs,',f'{dc_cut}-{min_dc}, {cnt},',f'{num+1}/{len_AND_list}, {exe_time}, {exe_time/(num+1)*len_AND_list}')
                    
if __name__ == "__main__":
    st = time.time()
    n = int(sys.argv[1])
    MC = int(sys.argv[2])
    Alg_one(n,MC)
    print(time.time()-st)