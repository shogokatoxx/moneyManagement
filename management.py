import json
from flask import Flask,render_template,redirect,request,Markup,escape
from datetime import datetime

application = Flask(__name__)
DATA_FILE = 'manage.json'

def save_data(forms,money,text,create_time):
    try:
        database = json.load(open(DATA_FILE,mode="r",encoding="utf-8"))
    except FileNotFoundError:
        database = []

    database.insert(0,{
    "forms":forms,
    "money":money,
    "text":text,
    "create_time":create_time.strftime("%Y-%m-%d")
    })
    json.dump(database,open(DATA_FILE,mode="w",encoding="utf-8"),indent=4,ensure_ascii=False)



def load_data():
    try:
        database = json.load(open(DATA_FILE,mode="r",encoding="utf-8"))
    except FileNotFoundError:
        database = []
    return database

@application.route('/')
def index():
    datas = load_data()
    return render_template('index.html',datas=datas)

@application.route('/save',methods=['POST'])
def save():
    forms = request.form.get('forms')
    money = request.form.get('money')
    text = request.form.get('text')
    create_time = datetime.now()
    save_data(forms,money,text,create_time)
    return redirect('/')

@application.route('/result')
def result():
    datas = load_data()
    return render_template('result.html',datas=datas)
    
@application.route('/delete/<int:pk>')
def delete(pk):
    try:
        database = json.load(open(DATA_FILE,mode="r",encoding="utf-8"))
    except FileNotFoundError:
        database = []
    for i,data in enumerate(database):
        i += 1
        if i == pk:
            data.clear()
    json.dump(database,open(DATA_FILE,mode="w",encoding="utf-8"),indent=4,ensure_ascii=False)
    return redirect('/')

@application.template_filter('nl2br')
def nl2br_filter(s):
    return escape(s).replace('\n',Markup('<br>'))

if __name__ == '__main__':
    application.run('0.0.0.0',8000,debug=True)
