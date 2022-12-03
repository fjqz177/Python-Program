import time
import re

'''
加入了输入数据判断是否为纯数字
可以自由选择加密或者解密
对文本显示进行了优化
'''

# 扩展欧几里的算法
# 计算 ax + by = 1中的x与y的整数解（a与b互质）

def ext_gcd(a, b):
    if b == 0:
        x1 = 1
        y1 = 0
        x = x1
        y = y1
        r = a
        return r, x, y
    else:
        r, x1, y1 = ext_gcd(b, a % b)
        x = y1
        y = x1 - a // b * y1
        return r, x, y


# 超大整数超大次幂然后对超大的整数取模
# (base ^ exponent) mod n

def exp_mode(base, exp, n):
    exp_array = bin(exp)[2:][::-1]
    ll = len(exp_array)
    result = 1
 
    for i in range(ll):
        if ('1'==exp_array[i]):
            result = (result * base) % n
        base = (base * base) % n
 
    return result % n

# 计算公钥和私钥的函数
def gen_key(p, q):
    n = p * q
    fy = (p - 1) * (q - 1)      # 计算与n互质的整数个数 欧拉函数
    e = 65537                    # 选取e   一般选取65537
    # generate d
    a = e
    b = fy
    r, x, y = ext_gcd(a, b)
    # 计算出的x不能是负数，如果是负数，说明p、q、e选取失败，不过可以把x加上fy，使x为正数，才能计算。
    if x < 0:
        x = x + fy
    d = x
    # 返回：   公钥     私钥
    return    (n, e), (n, d)

# 加密函数 m是被加密的信息 加密成为c
def encrypt(m, pubkey):
    n = pubkey[0]
    e = pubkey[1]
	
    time_start_e = time.time()
	
    c = exp_mode(m, e, n)
	
    time_end_e = time.time()
    time_e = time_end_e - time_start_e
    return c,time_e
# 解密函数 c是密文，解密为明文m
def decrypt(c, selfkey):
    n = selfkey[0]
    d = selfkey[1]
	
    time_start_d = time.time()
	
    m = exp_mode(c, d, n)
	
    time_end_d = time.time()
    time_d = time_end_d - time_start_d
	
    return m,time_d

def is_str(m):  
    an = re.match('[0-9]+$', m)  
    if an == None:
        print('密码必须是纯数字！')
        return False
    else:
        return True  

# 主程序
if __name__ == "__main__":
    while True:
        '''公钥私钥中用到的两个大质数p,q，都是1024位'''
        p = 106697219132480173106064317148705638676529121742557567770857687729397446898790451577487723991083173010242416863238099716044775658681981821407922722052778958942891831033512463262741053961681512908218003840408526915629689432111480588966800949428079015682624591636010678691927285321708935076221951173426894836169
        q = 144819424465842307806353672547344125290716753535239658417883828941232509622838692761917211806963011168822281666033695157426515864265527046213326145174398018859056439431422867957079149967592078894410082695714160599647180947207504108618794637872261572262805565517756922288320779308895819726074229154002310375209
        '''生成公钥私钥'''
        pubkey, selfkey = gen_key(p, q)
        '''需要被加密的信息转化成数字，长度小于秘钥n的长度，如果信息长度大于n的长度，那么分段进行加密，分段解密即可。'''
        m = input("请输入你想要处理的数据（必须是纯数字）\n")
        if is_str(m):
            m = int(m)
            print("待处理信息-->",m,"\n")
            '''信息加密，m被加密的信息，c是加密后的信息'''
            ask = input("请问是要进行加密（输入1）还是解密（输入2）？\n")
            if ask == "1":
                c,tme = encrypt(m, pubkey)
                print("被加密后的密文-->",c,"\n")
                print("加密用时",tme,"s\n")
                '''信息解密'''
            elif ask == "2":
                d,tmd = decrypt(m, selfkey)
                print("被解密后的明文-->",d)
                print("解密用时",tmd,"s\n")
            else:
                print("请输入“1”（加密）或者“2”（解密）！\n")