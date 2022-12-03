n = 3
pl = [2]

def lbbl(n):
    i = 1
    while (pl[i-1])**2 <=n:
        if n % (pl[i-1]) == 0:
            return False
        i = i + 1
    return True


while True:
    if lbbl(n) == True:
        pl.append(n)
        print(n)
    n = n + 2