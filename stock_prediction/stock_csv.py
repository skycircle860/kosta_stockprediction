import pymysql as my
import pandas as pd

def get_url(item_name):
    mycursor=mydb.cursor()
    sql = "select code from stock where name='{}'".format(item_name)
    mycursor.execute(sql)
    res=mycursor.fetchone()
    for code in res:
        pass
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    print("요청 URL = {}".format(url))
    return url

mydb=my.connect(
    host="192.168.0.110",
    user="bigdata",
    passwd="123123",
    db="project"
)
print(mydb)

mycursor=mydb.cursor()
mycursor.execute("select name from stock")
myresult=mycursor.fetchall()


for x in myresult:
    name = str(x)[2:-3]
    print(name)

    item_name=name
    url = get_url(item_name) 


    df = pd.DataFrame()

    for page in range(1, 100):
        pg_url = '{url}&page={page}'.format(url=url, page=page) 
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True) 
    

    df = df.dropna()
    
    if '/' in item_name:
        idx = item_name.index('/')
        item_name = item_name[:idx]+' '+ item_name[idx+1:]
    
    

    naming = 'stock_csv/{name}.csv'.format(name=item_name)

    df.to_csv(naming, sep=',', na_rep='NaN', encoding='utf-8')
    
