# 图形界面质数计算器 V1.1
# V1.1更新日志
# 加入质数序列输出
# 加入质数数量显示
# 源码

# 这个程序需要安装easygui库使用

import easygui as ezgui
import sys
import time

outpupFile = '质数输出.txt'

def zsjs():
		zhishu = int(ezgui.enterbox('请问您要计算多少以内的质数？'))
		time_start = time.time()
		num = []
		i=2
		for i in range(2,zhishu):
			j=2
			for j in range(2,i):
				if(i%j==0):
					break
			else:
				num.append(i)
		time_end = time.time()
		time_c = time_end - time_start 
		time_c = round(time_c,3)
		if time_c < 0.01:
			time_c = 0.01
		zhishushuliang = len(num)
		msg=f'计算结果如下\n用时{time_c}秒 质数有{zhishushuliang}个 质数数列已保存在程序所在的文件夹内的质数输出.txt'
		fo = open(outpupFile,'w')
		fo.write(str(num))
		fo.close()
		ezgui.textbox(msg,title,text = str(num))

while 1:
		title = "by 石光k一5"
		ok_button='继续'
		ezgui.msgbox("这是一个质数计算器\nby 石光k一5",title,ok_button='继续')
		msg =""
		ezgui.msgbox('''质数是指在大于1的自然数中，除了1和它本身以外不再有其他因数的自然数。''')
		choices = ["开始计算", "关于","退出"]
		choice = ezgui.buttonbox('by 石光k一5',title, choices)
		if choice == '开始计算':
			zsjs()

		if choice == '关于':
			ezgui.msgbox('by 石光k一5 制作',title,ok_button='继续使用')
			zsjs()
		
		if choice == '退出':
			sys.exit(0)
		
		if ezgui.ccbox('谢谢使用\nby 石光k一5', title,['继续使用','退出'],default_choice='继续使用',cancel_choice='退出程序'):
			pass
		else:
			sys.exit(0)