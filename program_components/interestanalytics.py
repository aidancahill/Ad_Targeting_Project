import json
from matplotlib.font_manager import json_load
import facebook
import pandas as pd
import requests

token = 'EAAQ1N6V3XmMBAIhNvefE1LjiIB147hftcvAuwkU6FXjXWZBLMcj9NcJZATo1R6LKG8s61BVbIP6eWyjaZA3iUdQBizHe7CrUNvNIM6yf8eaiZA1VZBaUPDtcrvMkunzO0jLoOTJWsZBMWy48NvCQzjOisvGTvpoWDTyJh7p3FVJ63AsgJRORAA'


interest = input("Enter an interest ")

adinterest = requests.get('https://graph.facebook.com/search?type=adinterest&q=[' + interest + ']&limit=10000&locale=en_US&access_token=' + token )

adinterest_json = adinterest.json()

print(adinterest_json)

df_interests = pd.json_normalize(adinterest_json['data'])

adinterest_sugg = requests.get('https://graph.facebook.com/search?type=adinterestsuggestion&interest_list=[''"' + interest + '"' ',' ']&limit=10000&locale=en_US&access_token=' + token )

adinterest_sugg_json = adinterest_sugg.json()

print(adinterest_sugg_json)

df_interests_sugg = pd.json_normalize(adinterest_sugg_json['data'])

df_all_interests = pd.concat([df_interests,df_interests_sugg], ignore_index=True, sort=False)

df_all_interests.to_csv(r'C:\Users\aidan\Documents\cont_ed\python projects\FacebookGraphAPI\'' + interest + '.csv', index=False)
