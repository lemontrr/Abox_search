import os
import time
import sys

def Jump(rans,counting,st,jumping,cut_dc,start_MC):
    n=8

    cnt = 0
    num = 0
    min_dc = 999
    for AND_c in rans:
        num+=1
        AND_Gate = [[AND_c[2*i],AND_c[2*i+1]] for i in range(start_MC)]
        for i in range(jumping):
            AND_Gate.append([0,0])
        
        output = [0]*start_MC
        S_bef = []
        for x in range(2**n):
            val = x
            for i in range(start_MC):
                output[i] = (bin(val&AND_Gate[i][0]).count('1')%2) & (bin(val&AND_Gate[i][1]).count('1')%2)
                val |= output[i]<<(i+n)
            out = 0
            for i in range(start_MC):
                out |= output[i]<<i
            S_bef.append(out)
        
        # jump two
        jump_ANDs = []
        for r_ndom in range(100):
            jump_AND = []
            for i in range(start_MC,start_MC+jumping):
                jump_AND.append(random.randrange(0,2**(n+i)))
                jump_AND.append(random.randrange(0,2**(n+i)))
            jump_ANDs.append(jump_AND)

        for r_ndom in range(100):
            for i in range(start_MC,start_MC+jumping):
                AND_Gate[i][0] = jump_ANDs[r_ndom][2*(i-start_MC)]
                AND_Gate[i][1] = jump_ANDs[r_ndom][2*(i-start_MC)+1]
            output = [0]*jumping
            S = []
            for x in range(2**n):
                val = (S_bef[x]<<n)|x
                for i in range(jumping):
                    output[i] = (bin(val&AND_Gate[start_MC+i][0]).count('1')%2) & (bin(val&AND_Gate[start_MC+i][1]).count('1')%2)
                    val |= output[i]<<(start_MC+i+n)
                out = S_bef[x]
                for i in range(jumping):
                    out |= output[i]<<(start_MC+i)
                S.append(out)

            ddt = [[0 for j in range(2**(start_MC+jumping))] for i in range(2**n)]
            for i in range(2**n):
                for j in range(i+1,2**n):
                    ddt[i^j][S[i]^S[j]] += 2
            dc = max([max(i) for i in ddt[1:]])
            if min_dc > dc:
                min_dc = dc
            if dc < cut_dc:
                cnt += 1
                with open(f'8bit_{start_MC+jumping}AND_under_{cut_dc}dc.txt','a') as f:
                    text = ''
                    for i in range(start_MC+jumping):
                        text += f'{AND_Gate[i][0]} {AND_Gate[i][1]} '
                    f.write(text + f'- {dc}\n')

    print(f'8bit_{start_MC+jumping}AND_under_{cut_dc}dc are {cnt} and min_dc = {min_dc}. Now is {counting}/{num}. time is', '%.2f'%(time.time()-st))

def low_num_dc(rans,counting,st,cut_dc,cut_dc_num,start_MC):
    n=8
    cnt = 0
    num = 0
    min_dc = 999
    for AND_c in rans:
        num+=1
        AND_Gate = [[AND_c[2*i],AND_c[2*i+1]] for i in range(start_MC)]
        AND_Gate.append([0,0])
        
        output = [0]*start_MC
        S_bef = []
        for x in range(2**n):
            val = x
            for i in range(start_MC):
                output[i] = (bin(val&AND_Gate[i][0]).count('1')%2) & (bin(val&AND_Gate[i][1]).count('1')%2)
                val |= output[i]<<(i+n)
            out = 0
            for i in range(start_MC):
                out |= output[i]<<i
            S_bef.append(out)
        
        # jump two
        jump_ANDs = []
        for r_ndom in range(100):
            jump_AND = []
            jump_AND.append(random.randrange(0,2**(n+start_MC)))
            jump_AND.append(random.randrange(0,2**(n+start_MC)))
            jump_ANDs.append(jump_AND)

        for r_ndom in range(100):
            AND_Gate[start_MC][0] = jump_ANDs[r_ndom][0]
            AND_Gate[start_MC][1] = jump_ANDs[r_ndom][1]

            output = [0]
            S = []
            for x in range(2**n):
                val = (S_bef[x]<<n)|x
                output[0] = (bin(val&AND_Gate[start_MC][0]).count('1')%2) & (bin(val&AND_Gate[start_MC][1]).count('1')%2)
                val |= output[0]<<(start_MC+n)
                out = S_bef[x]
                out |= output[0]<<start_MC
                S.append(out)
            ddt = [[0 for j in range(2**(start_MC+1))] for i in range(2**n)]
            for i in range(2**n):
                for j in range(i+1,2**n):
                    ddt[i^j][S[i]^S[j]] += 2
            dc = max([max(i) for i in ddt[1:]])
            dc_num = 0
            for i in range(2**n):
                for j in range(2**(start_MC+1)):
                    if ddt[i][j]>cut_dc:
                        dc_num += 1
            if min_dc > dc_num:
                min_dc = dc_num
            if dc_num < cut_dc_num:
                cnt += 1
                with open(f'8bit_{start_MC+1}AND_{dc}dc_{dc_num}dc_num.txt','a') as f:
                    text = ''
                    for i in range(start_MC+1):
                        text += f'{AND_Gate[i][0]} {AND_Gate[i][1]} '
                    f.write('\n')

    print(f'8bit_{start_MC+1}AND_{dc}dc_{dc_num}dc_num are {cnt} and min_dc = {min_dc}. Now is {counting}/{num}. time is', '%.2f'%(time.time()-st))

import random    
if __name__ == "__main__":
    start_MC = 5
    AND_list = []
    with open(f'8bit_{start_MC}AND_64dc.txt','r') as f:
        lines = f.readlines()
        lenth = len(lines)
        for line in lines:
            ANDs = list(map(int,line.split(' ')[:-1]))
            AND_list.append(ANDs)
    counting = 0
    st = time.time()
    while(True):
        counting += 1
        rans = [AND_list[random.randrange(0,lenth)] for i in range(100)]
        low_num_dc(rans,counting,st,cut_dc=32,cut_dc_num=30,start_MC=start_MC)
        # Jump(rans,counting,st,jumping=2,cut_dc=33,start_MC=start_MC)