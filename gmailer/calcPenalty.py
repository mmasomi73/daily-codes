import jdatetime
import pandas as pd

def percenter(day):
    if day <= 0:
        return 0
    if day == 1:
        return 0.1
    if day == 2:
        return 0.25
    if day == 3:
        return 0.45
    if day == 4:
        return 0.75
    if day >= 5:
        return 1

df = pd.read_csv('Lists.csv', encoding='utf-8')
diff_list = []
for index, row in df.iterrows():
    if len(str(row[1])) > 4:
        date = jdatetime.datetime.strptime(row[1], '%Y/%m/%d %H:%M')
        date = jdatetime.datetime.strptime(date.strftime("%Y/%m/%d"), '%Y/%m/%d')
        final = jdatetime.datetime.strptime('1400/01/11', '%Y/%m/%d')
        diff_list.append(percenter((date - final).days))
        row["Penalty"] = percenter((date - final).days)

df = df[df['Date'].notna()]
df["Penalty"] = diff_list

df.to_csv('List_penalty.csv', encoding='utf-8')
