import matplotlib.pyplot as plt
import os


def getFileSizeList(path):
    sizeList = []
    for filename in os.listdir(path):
        fullName = os.path.join(path, filename)
        size = os.path.getsize(fullName)
        sizeList.append(round(size / 1024, 2))
    return sizeList


def traversal_files(path, filesize=None):
    if filesize is None:
        filesize = []

    for item in os.scandir(path):
        if item.is_file():
            size = os.path.getsize(item)
            filesize.append(round(size / 1024 / 1024, 2))
        else:
            traversal_files(item.path, filesize)

    return filesize


y = traversal_files("D:\\我")

fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(9, 6))

# 第二个参数是柱子宽一些还是窄一些，越大越窄越密,数据多的时候将这个数值写大一些。
ax0.hist(y, 10000, density=True, histtype="bar", facecolor="yellowgreen", alpha=0.75)
##pdf概率分布图，一万个数落在某个区间内的数有多少个
ax0.set_title("pdf")

ax1.hist(
    y,
    10000,
    density=True,
    histtype="bar",
    facecolor="pink",
    alpha=0.75,
    cumulative=True,
    rwidth=0.8,
)
# cdf累计概率函数，cumulative累计。比如需要统计小于5的数的概率
ax1.set_title("cdf")

fig.subplots_adjust(hspace=0.4)

plt.show()
