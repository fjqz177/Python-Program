# 此程序需安装easygui库使用

import re
import string
import easygui as ezgui

def simple_replace(password, replace_word1, replace_word2, replace_word3):  
    count = 0  
    new_pass = ''  
    ori_table = 'abcdefghijklmnopqrstuvwxyz'  
    for obj in password:  
        table1 = str.maketrans(ori_table, replace_word1)  # 建立转子1的映射表
        table2 = str.maketrans(ori_table, replace_word2)  # 建立转子2的映射表
        table3 = str.maketrans(ori_table, replace_word3)  # 建立转子3的映射表
        new_obj = str.translate(obj, table1)  
        new_obj = str.translate(new_obj, table2)  
        new_obj = str.translate(new_obj, table3)  
        new_obj = reverse_word(new_obj)  
        reverse_table1 = str.maketrans(replace_word1, ori_table)  
        reverse_table2 = str.maketrans(replace_word2, ori_table)
        reverse_table3 = str.maketrans(replace_word3, ori_table)
        new_obj = str.translate(new_obj, reverse_table3)  
        new_obj = str.translate(new_obj, reverse_table2)  
        new_obj = str.translate(new_obj, reverse_table1)  
        new_pass += new_obj  
        replace_word1 = rotors(replace_word1)  
        count += 1  
        if count % 676 == 0:   
            replace_word3 = rotors(replace_word3)
        elif count % 26 == 0:  
            replace_word2 = rotors(replace_word2)
    return new_pass  
 
 
 
def is_str(password, replace_word1, replace_word2, replace_word3):  
    an = re.match('[a-z]+$', password)  
    if not type(password) == type(replace_word1) == type(replace_word2) == type(replace_word3) == type('a'):
        print('密码必须是字符串！')
        return False
    elif not an:
        print('字符串只能包含小写字母！')
        return False
    elif not len(replace_word1) == len(replace_word2) == len(replace_word3) == 26:
        print('替换码必须为26个字母！')
        return False
    else:
        return True  
 
 
def rotors(replace_word):  
    return replace_word[1:] + replace_word[0]
 
# 自反器很好设置的，只要设置一个字典，保证所有字母（26个）两两对应就可以了
 
 
def reverse_word(word):
    dic = {'a': 'n', 'b': 'o', 'c': 'p', 'd': 'q',
           'e': 'r', 'f': 's', 'g': 't', 'h': 'u',
           'i': 'v', 'j': 'w', 'k': 'x', 'l': 'y',
           'm': 'z', 'n': 'a', 'o': 'b', 'p': 'c',
           'q': 'd', 'r': 'e', 's': 'f', 't': 'g',
           'u': 'h', 'v': 'i', 'w': 'j', 'x': 'k',
           'y': 'l', 'z': 'm'}
    return dic[word]
 
while True:
    title = 'by 石光k一5'
    ezgui.msgbox('这是恩尼格码密码机',title)
    a_password = ezgui.enterbox('请输入明文加密或密文解密:',title)
    r_password1 = 'qwertyuiopasdfghjklzxcvbnm'  # 转子1，自己设置即可
    r_password2 = 'asdfqwerzxcvtyuiopghjklbnm'  # 转子2，自己设置即可
    r_password3 = 'poiuytrewqasdfghjklmnbvcxz'  # 转子3，自己设置即可
    if is_str(a_password, r_password1, r_password2, r_password3):
        msg=f'密文/明文如下:{simple_replace(a_password, r_password1, r_password2, r_password3)}'
        ezgui.textbox(msg,title)