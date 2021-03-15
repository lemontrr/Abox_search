import sys

def all_index(ints):
    large_int = [1]
    for i in range(len(ints)):
        large_int.append(large_int[i]*ints[i])
    all_of_index = []
    for i in range(large_int[-1]):
        ind = []
        for j in range(len(ints)):
            ind.append(int(i/large_int[-j-2]))
            i%=large_int[-j-2]
        all_of_index.append(ind[::-1])
    return all_of_index

def init_Abox(n):
    k = int((n-1)/2)+1
    with open(f'{n}bit_{k}AND__init.txt','w') as f:
        pass
    if n%2==0: j_range = [0]
    else     : j_range = [i for i in range(2,n+1)]
    for j in j_range:
        ints = []
        for i in range(1,k):
            if 2*i == j:
                ints.append(1<<(j+i))
            else:
                ints.append(1<<i)
            if 2*i+1 == j:
                ints.append(1<<(j+i))
            else:
                ints.append(1<<i)
        indexing = all_index(ints)
        all_text = ''
        for ind in indexing:
            _pass_ = False
            j_pass = 0
            text = '1 2 '
            for i in range(0,len(ind),2):
                if i+2 == j:
                    if ind[i]==0: 
                        _pass_ = True
                        continue
                    text += f'{ind[i]} {((ind[i+1]<<n)^(1<<(i+2)))} '
                    j_pass = 1
                elif i+3 == j:
                    if ind[i+1]==0: 
                        _pass_ = True
                        continue
                    text += f'{((ind[i]<<n)^(1<<(i+2)))} {ind[i+1]} '
                    j_pass = 1
                else:
                    if ind[i]>ind[i+1]:
                        _pass_ = True
                        continue
                    else:
                        text += f'{((ind[i]<<n)^(1<<(i+2-j_pass)))} {((ind[i+1]<<n)^(1<<(i+3-j_pass)))} '
            text += '\n'
            if _pass_: continue
            all_text += text
        with open(f'{n}bit_{k}AND__init.txt','a') as f:
            f.write(all_text)
    return

if __name__ == "__main__":
    n = int(sys.argv[1])
    init_Abox(n)
