#!/usr/bin/env python
# coding: utf-8

# In[11]:


from urllib.request import urlopen
import bs4
import datetime as dt
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
import csv
import os
import re
import requests
# 키워드 import
import sys
import urllib.request
import json

# 주식예측 import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation

import subprocess

from time import sleep

def date_format(d):
    d = str(d).replace('-','.')
    yyyy = int(d.split('.')[0])
    mm = int(d.split('.')[1])
    dd = int(d.split('.')[2])
    this_date = dt.date(yyyy,mm,dd)
    return this_date


def kospi200_list():
    
    global kospi

    BaseUrl = 'https://finance.naver.com/sise/entryJongmok.nhn?page='

    if os.path.exists('KOSPI200.csv'):
        os.remove('KOSPI200.csv')
    else:
        print("Sorry, I can not remove {} file.".format('KOSPI200.csv'))

    for i in range(1,22,1):
        try:
            url = BaseUrl + str(i)
            r = requests.get(url)
            soup =  BeautifulSoup(r.text,'lxml')
            items = soup.find_all('td',{'class':'ctg'})

            for item in items:
                txt = item.a.get('href')
                k = re.search('[\d]+',txt)
                if k:
                    code =  k.group()
                    name = item.text
                    data = code, name

                    with open('KOSPI200.csv','a') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)
        except:
            pass
        finally:
            temp_for_sort = []
            with open("KOSPI200.csv",'r') as in_file:
                for sort_line in in_file:
                    temp_for_sort.append(sort_line)
            with open('KOSPI200.csv','w') as out_file:
                seen = set()
                for line in temp_for_sort:
                    if line in seen: 
                        continue

                    seen.add(line)
                    out_file.write(line)


    with open("KOSPI200.csv",'r') as f:
        kospi = pd.read_csv(f, names=['code','name'])
    return kospi


def beforeday():
    
    global yester,yester2
    
    yester = dt.date.today() -  dt.timedelta(days=1)
    yester2 = dt.date.today() -  dt.timedelta(days=2)
    yester = str(yester)
    yester2 = str(yester2)
    return yester,yester2



# def keyword():
    
#     kospi200_list()
#     beforeday()
    
#     jnamestemp = kospi['name'].tolist()
#     jnames = []
#     for i in jnamestemp:
#         jnames.append("\""+i+"\"")
    
#     client_id = "yJNxYPr8d216pIiEBIaJ"
#     client_secret = "K92jjhZjSD"
#     url = "https://openapi.naver.com/v1/datalab/search";
    
#     temp = []
    
#     for jname in jnames:
#         body = "{\"startDate\":\""+yester2+"\",\"endDate\":\""+yester+"\",\"timeUnit\":\"date\",\"keywordGroups\":[{\"groupName\":\"한글\",\"keywords\":["+jname+"]}]}";

#         request = urllib.request.Request(url)
#         request.add_header("X-Naver-Client-Id",client_id)
#         request.add_header("X-Naver-Client-Secret",client_secret)
#         request.add_header("Content-Type","application/json")
#         response = urllib.request.urlopen(request, data=body.encode("utf-8"))
#         rescode = response.getcode()
#         if(rescode==200):
#             response_body = response.read()
#     #         response_body.decode('utf-8')
#         else:
#             print("Error Code:" + rescode)


#         toDict=json.loads(response_body.decode('utf-8'))
#         if toDict['results'][0]['data'][1]['ratio'] - toDict['results'][0]['data'][0]['ratio'] >= 25:
#             temp.append(jname)
            
#         # 리스트 요소에 포함된 큰따옴표 제거
#     tems = []
#     for tem in temp:
#         tem = tem.replace("\"","")
#         tem = tem.split()
#         tems.append(tem)

#     pJusicknames = tems

#     if os.path.exists('pi200.csv'):
#         os.remove('pi200.csv')

#     with open("pi200.csv","w",newline='') as out_writer:
#         writer = csv.writer(out_writer)
#         for pJusickname in pJusicknames:
#             writer.writerow(list(pJusickname),)
            
            
# keyword()


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

# subprocess.call (["/usr/bin/Rscript", "--vanilla", "/root/emotion_analysis_SiYeol.R"])
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------



def historical_index_naver2(index_cd, start_date='', end_date='', page_n=1, last_page=0):

    
    if start_date:
        start_date = date_format(start_date)
    else:
        start_date = dt.date.today()
    if end_date:
        end_date = date_format(end_date)
    else:
        end_date = dt.date.today()
    
    
    naver_index = 'https://finance.naver.com/item/sise_day.nhn?code='+index_cd+'&page='+str(page_n)
    
    source = urlopen(naver_index).read()
    source = bs4.BeautifulSoup(source, 'lxml')
    
    dates = source.find_all('span',class_='tah p10 gray03')
    prices = source.find_all('td',class_='num')
    for n in range(len(dates)):
        
        if dates[n].text.split('.')[0].isdigit():
            #날짜처리
            this_date = dates[n].text
            this_date = date_format(this_date)
            
            if this_date <= end_date  and this_date >= start_date:
                
                #종가처리
#                 this_close = prices[n*6].text

#                 this_close = this_close.replace(',','')
#                 this_close = float(this_close)
                
                #고가처리
                this_high = prices[n*6+3].text

                this_high = this_high.replace(',','')
                this_high = float(this_high)
                
                #저가처리
                this_low = prices[n*6+4].text

                this_low = this_low.replace(',','')
                this_low = float(this_low)

                #딕셔너리에 저장
                high[this_date] = this_high
                low[this_date] = this_low
            elif this_date < start_date:
                #start_date 이전이면 함수 종료
#                 historical_df = {'high':high,'low':low}
                return high,low

        #페이지 내비게이션
    if last_page == 0:
        last_page = source.find('td',class_='pgRR').find('a')['href']
        last_page = last_page.split('&')[1]
        last_page = last_page.split('=')[1]
        last_page = int(last_page)
            
        #다음 페이지 호출
    if page_n < last_page:
        page_n = page_n + 1
        historical_index_naver2(index_cd, start_date, end_date, page_n, last_page)
            
    return high,low


def final_pred():
    
    subprocess.call (["/usr/bin/Rscript", "--vanilla", "/root/emotion_analysis_SiYeol.R"])
    
    sleep(3)
    
    with open("Rjname.csv",'r') as f:
        rnames = pd.read_csv(f)
    rnames = rnames[rnames.columns.tolist()[0]].tolist()
    print(rnames)
    kospi200_list()
    inDF = {}
    for rname in rnames:
        rcode = str(int(kospi[kospi['name'] == rname]['code'].values)).zfill(6)
#         high = dict()
#         low = dict()
        # historical_df = dict()
        historical_index_naver2(rcode,str(dt.date.today()-dt.timedelta(days=365*5)))
        temp = {'고가':high,'저가':low}
        highlow = pd.DataFrame(temp)
        inDF[rname] = highlow
    
    
    # naming = "2019-6-12/{name}.csv".format(today=today, name=name)
    for idx,rname in enumerate(rnames):

        data = inDF[rname]

        high_prices = data['고가'].values
        low_prices = data['저가'].values
        mid_prices = (high_prices + low_prices) / 2

        seq_len = 50
        sequence_length = seq_len + 1

        result = []
        for index in range(len(mid_prices) - sequence_length):
            result.append(mid_prices[index: index + sequence_length])





        # result값을 정규화(처음날로 나눈값)한 값을 넣어준다
        normalized_data = []
        for window in result:
            normalized_window = [((float(p) / float(window[0])) - 1) for p in window]
            normalized_data.append(normalized_window)
        # 정규화된 값을 다시 result로 넣는다.
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


        if idx == 0:
            # 층들의 스택을 쌓기위한 빈 모델을 생성  
            model = Sequential() 
            # Sequential에 있는 LSTM이라는 모듈 사용
            # 유닛의 수가 50개 라는 뜻
            # input_shape : input size를 50,1로 지정해 준다
            # input_shape : 입력데이터의 모양을 알려준다(튜플 형태)
            model.add(LSTM(50, return_sequences=True, input_shape=(50, 1)))
            # 유닛의 수가 64개 라는 뜻(조정하면서 성능 테스트)
            model.add(LSTM(64, return_sequences=False))
            # output으로 나오는 것(1개)
            model.add(Dense(1, activation='linear'))
            # lost function(손실 함수) 
            # 손실함수 : 인공신경망에서 학습을 통해 최적의 가중치 매개변수를 결정하기 위한 
            #            기준으로 사용하는 함수
            # 손실함수의 결과값을 가장 작게 만드는 것이 신경망 학습의 목표
            # 손실함수의 결과값을 작게 만들기 위해서 가중치 매개변수를 조절해가는 과정이 학습 과정
            # mse(Mean Squared Error)를 사용 :  평균제곱오차
            model.compile(loss='mse', optimizer='rmsprop')
            # 모델 출력  
            model.summary()



            # 트레이닝 코드
            # batch_size : 한번에 몇 개씩 묶어서 학습시킬것인가
            # epochs : 몇 번을 반복학습 시킬것인가
            model.fit(x_train, y_train,
                validation_data=(x_test, y_test),
                batch_size=10 ,
                epochs=20)




        lastval = float(result[-1][-1])
        predval=float(model.predict(result[-1][1:].reshape(-1,50,1)))

        if lastval < predval:
            incname.append(rname)

        print(incname)

final_pred()


# In[ ]:



