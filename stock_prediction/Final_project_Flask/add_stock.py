import pymysql as my
import pandas as pd

def get_url(item_name):
    mycursor=mydb.cursor()
    sql = "select code from stoke where name='{}'".format(item_name)
    mycursor.execute(sql)
    res=mycursor.fetchone()
    for code in res:
        pass
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    print("요청 URL = {}".format(url))
    return url

mydb=my.connect(
    host="192.168.0.21",
    user="bigdata",
    passwd="123123",
    db="project"
)
print(mydb)

mycursor=mydb.cursor()
mycursor.execute("select name from stoke")
myresult=mycursor.fetchall()

for x in myresult:
    name = str(x)[2:-3]
    print(name)

    item_name=name
    url = get_url(item_name) 


    df = pd.DataFrame()


    for page in range(1, 2):
        pg_url = '{url}&page={page}'.format(url=url, page=page) 
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True) 

    

    df = df.dropna()
    df2 = pd.read_csv(naming, engine='python')




    date = df['날짜'].values
    end_p = df['종가'].values
    yest = df['전일비'].values
    start_p = df['시가'].values
    high_p = df['고가'].values
    low_p = df['저가'].values
    trade = df['거래량'].values

    #print([date[0],end_p[0],yest[0],start_p[0],high_p[0],low_p[0],trade[0]])

    df2 = df2.sort_index(ascending=False)
    df2.loc[len(df2),:] = [0,date[0],end_p[0],yest[0],start_p[0],high_p[0],low_p[0],trade[0]]
    df2.to_csv("temp.csv", sep=',', na_rep='NaN', encoding='utf-8')
    df3 = pd.read_csv("temp.csv", engine='python')

    df3 = df3.sort_index(ascending=False)

    del df3['Unnamed: 0']
    del df3['Unnamed: 0.1']
    
    if '/' in item_name:
        idx = item_name.index('/')
        item_name = item_name[:idx]+' '+ item_name[idx+1:]
    
    naming = '{0}.csv'.format(item_name)
    df3.to_csv("temp.csv", sep=',', na_rep='NaN', encoding='utf-8')
