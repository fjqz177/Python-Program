from time import time

def lbbl(n):
    i = 1
    while (pl[i-1])**2 <=n:
        if n % (pl[i-1]) == 0:
            return False
        i = i + 1
    return True

if __name__=='__main__': 
    n = 3
    pl = [2]
    nei = 1000000
    nei2 = int(nei/2)
    t1 = time()
    for z in range(nei2):
        if lbbl(n):
            pl.append(n)
        n = n + 2
    t2 = time()
    tt = t2 - t1
    print(len(pl))
    print("{}以内素数共{}个:".format(nei,len(pl)))
    print("共耗时",tt,"秒")#1.7