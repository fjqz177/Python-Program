import os
import sys
import easygui as ezgui
import time

main = r"primecount.exe"

def p(nm):
    return int(os.popen(main+" "+str(nm)).read())

def zsjs():
        zhishu = int(ezgui.enterbox("请问您要计算多少以内的质数？"))
        time_start = time.time()
        zhishushuliang = p(zhishu)
        time_end = time.time()
        time_c = time_end - time_start 
        time_c = round(time_c,3)
        if time_c < 0.01:
            time_c = 0.01
        msg=f"计算结果如下\n一共用时{time_c}秒 {zhishu}以内有{zhishushuliang}个质数"
        ezgui.msgbox(msg,title,ok_button="继续使用")

while True:
    title = "By fjqz177"
    ezgui.msgbox("这是一个质数数量计算器 By fjqz177\n质数是指在大于1的自然数中，除了1和它本身以外不再有其他因数的自然数。",title,ok_button="继续")
    choices = ["开始计算", "关于","退出"]
    choice = ezgui.buttonbox("By fjqz177",title, choices)
    if choice == "开始计算":
        zsjs()
    if choice == "关于":
        ezgui.msgbox("By fjqz177 制作",title,ok_button="继续使用")
        zsjs()
    if choice == "退出":
        sys.exit(0)
    if ezgui.ccbox("谢谢使用\nBy fjqz177", title,["继续使用","退出"],default_choice="继续使用",cancel_choice="退出程序"):
        pass
    else:
        sys.exit(0)