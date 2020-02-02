from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import os,sys
from datetime import datetime, date, timedelta
#import nagisa

data = {
    'name': '',
    'login': False,
    'dir':''
}

value = sys.argv

dt_now = datetime.now()

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/get', methods=['GET', 'POST'])
def Get():
    TARGET_DIR = data['dir']
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
        text = '何もないよ！'
        return render_template('yesterday.html',text=text)
    for y in files:
        if(y[-4:] == '.txt'):     #ファイル名の後ろ4文字を取り出してそれが.txtなら
            texts.append(y)  #リストに追加
    if texts == []:
        text = '何もないよ！'
        return render_template('yesterday.html',text=text)
    else:
        text_ = []
        for f in texts:
            with open(path+f, encoding='utf-8') as f_:
                text.append(f_.read())
        print('昨日のこの時間書き込んだことは...\n')
        text = '\n'.join(text_)
        return render_template('yesterday.html',text=text)



@app.route('/post', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        data['name'] = name
        data['login'] = True
        TARGET_DIR = "data/{Name}".format(Name=name)
        data['dir'] = TARGET_DIR
        if not os.path.isdir(TARGET_DIR):
            os.makedirs(TARGET_DIR)
            text = '{Name}さんはじめまして！'.format(Name=name)
            return render_template('choice.html',text=text)
        else:
            text = '{Name}さんいらっしゃい！'.format(Name=name)
            return render_template('choice.html',text=text)
    else:
        return redirect(url_for('login'))

@app.route('/w', methods=['GET', 'POST'])
def write_():
    return render_template('write.html')



#実行終了
#sys.exit()
@app.route('/posts', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        text_ = request.form['name']
        TARGET_DIR = data['dir']
        filename = '{Dir}/{Day}/{Time}/{FileName}.txt'.format(Dir=TARGET_DIR,Day=dt_now.strftime('%Y-%m-%d'),Time=dt_now.strftime('%H'),FileName=dt_now.strftime('%H-%M-%S'))
        file_path = os.path.dirname(filename)
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        with open(filename, 'w') as f:
            f.write(text_)
        text = '書き込めたよ！'
        return render_template('choice.html',text=text)
    else:
        return redirect(url_for('choice'))






#コマンドライン入力
#print('あなたの名前を教えてください。')
#your_name = input('>> ')
#print(your_name)




#while True:
#    main()


if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run()#(host='0.0.0.0') # どこからでもアクセス可能に
