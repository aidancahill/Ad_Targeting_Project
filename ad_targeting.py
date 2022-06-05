"""Aidan Cahill 6/5/2022
   Ad Targeting Project"""
import csv                     
import requests
import json
import pandas as pd
from matplotlib.font_manager import json_load
import plotly.express as px
import facebook
from pytrends.request import TrendReq

"""Import statements to include libraries to handle csv files, API requesting, json files, pandas library
    matplotlib library although there is no use of this library in the program it uses the json load function 
    to load json files, plotlyt is not used as well but is used for graph plotting, facebook library to access the api properly
    and the pytrends library to access the unofficial pytrends api"""

"""The main use of this program is to function as an ad targeting research tool that allows the user to input the 
    the specific key word or broad term used to understand customers behaviors online. Specificall the program 
    takes input from the user and generates two csv files, one with related queries and suggestions that google 
    yields within the scope of the inputed term. Second csv file is output related to customer behavior interests
    within the scope of facebook """

def google_trends(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)
    """specifying to google trends api that this payload of related queries is specific to the us and in the scope of time zone specific to the us"""
    kw_list = [keyword]
    """the keyword is the user inputted is stored in the kw_list array"""
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
    """Buuilding of the pytrends payload with the users keyword input and specifies from now and 5 years in the past"""
    df_rq = pytrends.related_queries()
    """storing the pytrends payload into a pandas dataframe"""
    sugg = pytrends.suggestions(keyword = "'" + keyword + "'")
    """variable storing pytrends suggested items based on the users keyword input"""
    df_sugg = pd.DataFrame(sugg, columns=['title'])
    """storing suggestions into a pandas dataframe"""
    df_sugg.rename(columns = {'title':'query'}, inplace = True)
    """rename the suggestions dataframe  column with suggestions from title to query to match the column name of the related queries dataframe column name"""
    df_rq.values()

    allkeywords = []
    """this next for loop designates a length based on the related queries dataframe and loops through to combine the 
        the top related queries to the rising related queries into a single all encompassing dataframe. As well as combining 
        the suggested queries into the same dataframe to create a single dataframe called allkeywords to house the entirety 
        of the keywords related to the users input"""
    for i in range(len(list(df_rq.values()))):

        top = list(df_rq.values())[i]['top']
        rising = list(df_rq.values())[i]['rising']


        df_top = pd.DataFrame(top)
        df_rising = pd.DataFrame(rising)
        
        allkeywords.append(df_top)
        allkeywords.append(df_rising)
        allkeywords.append(df_sugg)

    allkeywords = pd.concat(allkeywords, axis=0)

    allkeywords.reset_index(drop=True, inplace=True)

    df_rq_phrs = allkeywords.copy()

    df_rq_exct = allkeywords.copy()
    """this next for loop is a feature of the program for google ads specfically to add on the left and right each side of the strings
        within the all keywords data frame both double quotes " and brackets []. The allkeywords datframe contains a copy of the original 
        top, rising, and suggested queries, and two other copies of the same data but adds the double quotes to one copy and brackets to another"""
    for i in range(len(df_rq_phrs)):
        df_rq_phrs.loc[i,'query'] = '"' + df_rq_phrs.loc[i,'query'] + '"'
        df_rq_exct.loc[i,'query'] = '[' + df_rq_exct.loc[i,'query'] + ']'      


    allkeywords = pd.concat([allkeywords,df_rq_phrs,df_rq_exct], ignore_index=True, sort=False)
    """combine all data into a single source and output it into csv housed in the programs directory"""
    allkeywords.to_csv(r'C:\Users\aidan\Documents\cont_ed\python projects\ad_targeting_project\'' + keyword + '_google.csv', columns=['query'], index=False, quoting=csv.QUOTE_NONE)




def facebook_interests(keyword):
    token = '*********************************************************************'
    """assigns the users input to interest variable and make an api call to the facebook graph api to relay what interest inside facebook relate to the users input"""
    interest = keyword

    adinterest = requests.get('https://graph.facebook.com/search?type=adinterest&q=[' + interest + ']&limit=10000&locale=en_US&access_token=' + token )
    """specify a variable that contains the api response of a json file"""
    adinterest_json = adinterest.json()
    """create a pandas dataframe thats houses this information"""
    df_interests = pd.json_normalize(adinterest_json['data'])
    """make a second api request to the graphi api of suggested interests that relates to the users input"""
    adinterest_sugg = requests.get('https://graph.facebook.com/search?type=adinterestsuggestion&interest_list=[''"' + interest + '"' ',' ']&limit=10000&locale=en_US&access_token=' + token )

    adinterest_sugg_json = adinterest_sugg.json()
    """create a variable that holds the json file and put it into a pandas dataframe"""
    df_interests_sugg = pd.json_normalize(adinterest_sugg_json['data'])
    """combine all the dataframes into a single dataframe"""
    df_all_interests = pd.concat([df_interests,df_interests_sugg], ignore_index=True, sort=False)
    """output the data into a csv file stored in the programs directory"""
    df_all_interests.to_csv(r'C:\Users\aidan\Documents\cont_ed\python projects\ad_targeting_project\'' + interest + '_facebook.csv', columns= ['name'], index=False)

"""main body of the program where the user is asked for a keyword that is the main variable used by both functions"""
keyword = input("Enter a Keyword ")

"""call both functions using the users input"""
google_trends(keyword)

facebook_interests(keyword)