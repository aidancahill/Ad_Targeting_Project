
import pandas as pd
import matplotlib as plt
import plotly.express as px
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

keyword = input("Enter a Keyword ")

kw_list = [keyword]

pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

df_rq = pytrends.related_queries()

df_rq.values()

allkeywords = []

for i in range(len(list(df_rq.values()))):

    top = list(df_rq.values())[i]['top']
    rising = list(df_rq.values())[i]['rising']


    df_top = pd.DataFrame(top)
    df_rising = pd.DataFrame(rising)
    
    allkeywords.append(df_top)
    allkeywords.append(df_rising)


allkeywords = pd.concat(allkeywords, axis=0)

allkeywords.reset_index(drop=True, inplace=True)

df_rq_phrs = allkeywords.copy()

df_rq_exct = allkeywords.copy()

for i in range(len(df_rq_phrs)):
    df_rq_phrs.loc[i,'query'] = '"' + df_rq_phrs.loc[i,'query'] + '"'

for i in range(len(df_rq_exct)):
    df_rq_exct.loc[i,'query'] = '[' + df_rq_exct.loc[i,'query'] + ']'


allkeywords = pd.concat([allkeywords,df_rq_phrs,df_rq_exct], ignore_index=True, sort=False)

allkeywords.to_csv(r'C:\Users\aidan\Documents\cont_ed\python projects\ad_targeting_project\'' + keyword + '.csv', columns=['query'], index=False)


'''fig = px.line(data, x="date", y=[keyword], title='Keyword Web Search Interest Over Time')
fig.show()'''