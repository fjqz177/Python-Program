from time import time

def sieve(n):
    prime = [True for i in range(n+1)]
    p = 2
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n+1, p):
                prime[i] = False
        p += 1
    for p in range(2, n):
        if prime[p]:
            pl.append(p)

if __name__=='__main__':
    pl=[]
    n = 1000000
    t1 = time()
    sieve(n)
    t2 = time()
    tt = t2 - t1
    print(n)
    print("{}以内素数共{}个:".format(n,len(pl)))
    print("共耗时",tt,"秒")#0.12