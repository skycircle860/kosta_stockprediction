# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:32:33 2019

@author: KOSTA
"""

import pymysql as my
import pandas as pd
import tweepy
import time

def deduplication(name):
    
    input_file = "/root/SNS_Crawling/orign/"+name+"_orign"+".txt"
    output_file = "/root/SNS_Crawling/deduplication/"+name+"_dedupl"+".txt"
    df=""
    
    try:
        with open(input_file, encoding='euc-kr') as i:
            df=pd.DataFrame([x.replace("\n","") for x in list(i)])
        #print(df)
        df2 = df.drop_duplicates()
        #print(df2)

        df2.to_csv(output_file,encoding='euc-kr', index=False, header=False)
        
    except BaseException as e:
        print("Error on_data : %s" % str(e))

consumer_key = 'G0HC5EgeBskSGm61PHjV6G5Bs' #(API key)
consumer_secret = 'GX9poaNuIGJOO14HGLmxb3rOLHYinARcaQT53HQVnwS1bHO9ck' #(API secret key)
access_token = '1123132326823645184-bT2kUoYwimOSOOuXcjzkjVw0Jyna5Y' #(Access token)
access_token_secret = '9VQm7P33uY0j5Hl0WlBnglxNWgBYRf73rbploLVYWFeX0' #(Access token secret)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

mydb=my.connect(
    host="192.168.0.21",
    user="bigdata",
    passwd="123123",
    db="project",
    charset='utf8'
)
print(mydb)
mycursor=mydb.cursor()
mycursor.execute("select name from stoke")
myresult=mycursor.fetchall()

#print(myresult)
#res = list(myresult)

#print(res)
while 1:
    for x in myresult:
        name = str(x)[2:-3]
        #print(name)
        public_tweets = api.search(name)

        for tweet in public_tweets:
            print(tweet.text)
            try:
                print(tweet.text)
                output=open("/root/SNS_Crawling/orign/"+name+"_orign"+".txt","a",encoding='euc-kr')
                output.write(tweet.text)
                output.write("\n")
                output.close()
                deduplication(name)
            except BaseException as e:
                print("Error on_data : %s" % str(e))
    time.sleep(1800)
