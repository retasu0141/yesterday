from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import os,sys
from datetime import datetime, date, timedelta
#import nagisa

value = sys.argv

dt_now = datetime.now()

# 自身の名称を app という名前でインスタンス化する
#app = Flask(__name__)

def Get(TARGET_DIR):
    today = dt_now.today()
    yesterday = today - timedelta(days=1)
    #print(datetime.strftime(yesterday, '%Y-%m-%d'))
    path = '{Dir}/{Day}/{Time}/'.format(Dir=TARGET_DIR,Day=datetime.strftime(yesterday, '%Y-%m-%d'),Time=dt_now.strftime('%H'))
    files = []
    texts = []
    try:
        for x in os.listdir(path):
            if os.path.isfile(path + x):
                files.append(x)
    except:
        return '何もないよ！'
    for y in files:
        if(y[-4:] == '.txt'):     #ファイル名の後ろ4文字を取り出してそれが.txtなら
            texts.append(y)  #リストに追加
    if texts == []:
        return '何もないよ！'
    else:
        text = []
        for f in texts:
            with open(path+f, encoding='utf-8') as f_:
                text.append(f_.read())
        #print('\n'.join(text))
        return '\n'.join(text)

command = """～コマンド一覧～
・コマンド一覧     この文章を出します
・終了             終了します
・書き込み         今思ってることを書き込み記録します
・昨日の今         昨日の今の時間に書き込んだ記録を表示させます(未実装)
・XXXX-XX-XX X     指定した日時の記録を表示します(未実装)
(例:2020-01-01 12 → 2020年1月1日12時)"""

if len(value) > 1:
    name = value[1]
    TARGET_DIR = "data/{Name}".format(Name=name)
    if not os.path.isdir(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print('{Name}さんはじめまして！'.format(Name=name))
    else:
        print('{Name}さんいらっしゃい！'.format(Name=name))
else:
    print('あなたの名前を教えてください')
    name = input('>> ')
    TARGET_DIR = "data/{Name}".format(Name=name)
    if not os.path.isdir(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print('{Name}さんはじめまして！'.format(Name=name))
        pass
    else:
        print('{Name}さんいらっしゃい！'.format(Name=name))
        pass
print('昨日のこの時間書き込んだことは...\n')
print(Get(TARGET_DIR))


#実行終了
#sys.exit()

def write(data):
    filename = '{Dir}/{Day}/{Time}/{FileName}.txt'.format(Dir=TARGET_DIR,Day=dt_now.strftime('%Y-%m-%d'),Time=dt_now.strftime('%H'),FileName=dt_now.strftime('%H-%M-%S'))
    file_path = os.path.dirname(filename)
    if not os.path.isdir(file_path):
        os.makedirs(file_path)
    with open(filename, 'w') as f:
        f.write(data)
    print('書き込めたよ！')



def main():
    print('\nなにする？\n分からなかったら"コマンド一覧"って言ってね！')
    reply = input('>> ')
    if reply == 'テスト':
        print(TARGET_DIR)
    if reply == '書き込み':
        print('記録する分を書いてね')
        comment = input('>> ')
        write(comment)
    elif reply == 'コマンド一覧':
        print(command)
    elif reply == '終了':
        print('おつかれさまです！')
        sys.exit()
    else:
        pass



#コマンドライン入力
#print('あなたの名前を教えてください。')
#your_name = input('>> ')
#print(your_name)




while True:
    main()
