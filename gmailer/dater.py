import jdatetime
import datetime
import pandas as pd

start_date_1 = jdatetime.datetime(1399, 6, 22)
start_date_2 = jdatetime.datetime(1399, 6, 24)

weeker = jdatetime.timedelta(days=7)
date_list = []

for i in range(40):
    # print(start_date.strftime("%m/%d"))
    date_list.append(start_date_1.strftime("'%m-%d"))
    start_date_1 = start_date_1 + weeker

    date_list.append(start_date_2.strftime("'%m-%d"))
    start_date_2 = start_date_2 + weeker

df = pd.DataFrame(date_list)
df.to_csv('date.csv', encoding='utf-8')
