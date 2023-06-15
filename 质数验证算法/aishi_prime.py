from time import time
from rich.progress import track

def ess(n):
    pl = [2]
    Td = [True] * (n + 1)
    for i in track(range(3, n + 1, 2)):
        if Td[i]:
            pl.append(i)
            for j in range(i ** 2, n + 1, i * 2):
                Td[j] = False
    return pl

if __name__ == "__main__":
    nei = 1000000
    t1 = time()
    pl = ess(nei)
    t2 = time()
    tt = t2 - t1
    print("{}以内素数共{}个:".format(nei,len(pl)))
    print("共耗时{}秒".format(tt))#0.16s for 1000000