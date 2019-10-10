#서버 ////////////////////
import pymysql as my
from flask import Flask, render_template, request
from urllib.request import urlopen
import urllib.request as req
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation
import subprocess
import csv


#import datetime
from datetime import datetime

mydb=my.connect(
    host="192.168.0.110",
    user="bigdata",
    passwd="123123",
    db="project"
)
print(mydb)

app=Flask(__name__)

@app.route('/') #라즈베리파이IP:5000/로 접속시 index.html으로 연결
def index():
	return render_template('index2.html')

@app.route('/about') 
def about():
	return render_template('about.html')

@app.route('/main') 
def main():
	return render_template('main.html')

@app.route('/fail')
def fail():
        return render_template('fail.html')

@app.route('/qna') 
def qna():
	return render_template('qna.html')

@app.route('/search/<txt>')
def search_stock(txt):
	print(txt)
	sql = "select name from stock where name like '%{}%'".format(txt)
	res = get_list(sql)
	
	return res

@app.route('/analysis/<name>')
def analysis(name):
	print(name)
	
	res = stock_analysis(name)
	
	return "1"



@app.route('/detail/<name>')
def detail_stock(name):
	print(name)
	code = get_code(name)
	res = get_stock_info(code,name)
	
	return res

def get_list(sql):
    mycursor=mydb.cursor()
    mycursor.execute(sql)
    res=mycursor.fetchall()
    
    stock_list = "";
    for x in res:
        name = str(x)[2:-3]
        stock_list = stock_list + "," + name
    return stock_list

def get_code(name):
    mycursor=mydb.cursor()
    sql = "select code from stock where name='{0}'".format(name)
    mycursor.execute(sql)
    res=mycursor.fetchone()

    code = str(res)[2:-3]
    return code

def get_stock_info(code,name):
    url = "https://finance.naver.com/item/main.nhn?code={}".format(code)
    html=urlopen(url)

    #HTML 분석하기
    soup=BeautifulSoup(html.read(),"html.parser")
    
    info_list=soup.find_all(class_="rate_info")
    data = info_list[0]
    data_list = data.text.split("\n")

    info = ""

    for x in data_list:
        if(x !=''):
            info += x+"@"
    info += code+"@"
    
    
    
    
    try:
        table = get_stock_table(code)
    except:
        table = " "
        
    info += table+"@"
    
    
    cpresult = searchCpPegInfo(name)
    cpname = searchCheck(cpresult)
    info += cpname+"@"


    sns = getTwitter(name)
    print(sns)
    info += sns+"@"

    #print(info)

    #print(info)
    
    
    return info


def getTwitter(name):

    f = open("/root/SNS_Crawling/corporation.txt", 'w')
    f.write(name+"\n")
    f.close()

    subprocess.call (["/usr/bin/Rscript", "--vanilla", "/root/emotion_analysis.R"])

    f = open('/root/SNS_Crawling/result.csv', 'r', encoding='utf-8')
    twitter = list(csv.reader(f))[1][1]
    f.close()

    return twitter



def searchCpPegInfo(name):
    mycursor=mydb.cursor()
    mycursor.execute("select peg from stock_data_table where cp_name = '{}'".format(name))
    myresult=mycursor.fetchall()
    return myresult

def searchCheck(cpresult):
    if len(cpresult) == 0:
        cpname = "PEG 값이 없습니다. 신규 상장주이거나 투자대상으로 적합하지 않습니다."
        return cpname
    
    sliceindex = str(cpresult).find(",")
    cpname = str(cpresult)[2:sliceindex]
    return cpname


def get_stock_table(code):
   #cpcode = '005930'
   #cpname = "삼성전자"
    URL = "https://finance.naver.com/item/main.nhn?code={code}".format(code=code)

    html = requests.get(URL).text

    soup = BeautifulSoup(html, 'html.parser')

    finance_html = soup.select_one('div.section.cop_analysis div.sub_section')

    
    #print(finance_html)

    th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
    annual_date = th_data[3:7]
    quarter_date = th_data[7:13]

    finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:]

    finance_data = [item.get_text().strip() for item in finance_html.select('td')]



    finance_data = np.array(finance_data)
    finance_data.resize(len(finance_index), 10)

    finance_date = annual_date + quarter_date


    finance = pd.DataFrame(data=finance_data[0:,0:], index=finance_index,
                          columns=finance_date)

    return finance.to_html()



def stock_analysis(name):
    #name = "LG전자"
    naming = "stock_csv/{name}.csv".format(name=name)
    data = pd.read_csv(naming,  engine='python')
    data.head()
    high_prices = data['고가'].values
    low_prices = data['저가'].values
    mid_prices = (high_prices + low_prices) / 2
    seq_len = 50
    sequence_length = seq_len + 1
    result = []
    for index in range(len(mid_prices) - sequence_length):
        result.append(mid_prices[index: index + sequence_length])
    

    
    normalized_data = []
    for window in result:
        try:
            normalized_window = [((float(p) / float(window[0])) - 1) for p in window]
        except:
            normalized_window = 0

        normalized_data.append(normalized_window)
        
    result = np.array(normalized_data)
    
    # split train and test data
    row = int(round(result.shape[0] * 0.9))
    train = result[:row, :]
    np.random.shuffle(train)
    
    x_train = train[:, :-1]
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    y_train = train[:, -1]
    
    x_test = result[row:, :-1]
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    y_test = result[row:, -1]
    
    x_train.shape, x_test.shape


    model = Sequential() 
    model.add(LSTM(50, return_sequences=True, input_shape=(50, 1)))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer='rmsprop')
    model.summary()


    model.fit(x_train, y_train,
        validation_data=(x_test, y_test),
        batch_size=10,
        epochs=20)



    pred = model.predict(x_test)

    fig = plt.figure(facecolor='white', figsize=(20, 10))
    ax = fig.add_subplot(111)
    ax.plot(y_test, label='True')
    ax.plot(pred, label='Prediction')
    ax.legend()
    img_name = "static/stock_img/{}.png".format(name)
    plt.savefig(img_name, dpi=350)
    plt.show()
    return "1"




if __name__=='__main__':
	print('WebServer Start')
	app.run(host='192.168.0.110')

