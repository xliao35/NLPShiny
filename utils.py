from nltk.corpus import stopwords
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from datetime import date
from cleantext import clean
import numpy as np
import re

ps = PorterStemmer()
wl = WordNetLemmatizer()

def checkInput(df):
    cols = list(df.columns)
    match_set = ["username", "comment_body","comment_created_at"] # Matched Columns

    if len(cols) != len(match_set):
        return False
    for col in cols:
        if col.lower().strip() not in match_set:
            return False
    return True

def transform(df,method, stop_choice, digital_choice):
    stop = stopwords.words('english')
    
    df["comment_body"] = df['comment_body'].fillna('')
    for i in df['comment_body'].index:
        df['comment_body'][i] = clean(df['comment_body'][i], no_emoji=True)

    df["comment_body"] = df['comment_body'].str.replace('[^\w\s]','')
    if digital_choice == 'Remove':
        df["comment_body"] = df['comment_body'].str.replace('\d+', '')
        
    if method == "Stemming":
        if stop_choice == 'Remove':
            df["comment_no_Stopwords"] = df["comment_body"].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
            df["transformation"] = df["comment_no_Stopwords"].apply(lambda x: [ps.stem(y) for y in x])
            
        else:
            df["transformation"] = df["comment_body"].apply(lambda x: [ps.stem(y) for y in x]) 
        for i in df['transformation'].index:
            df['transformation'][i] = ''.join(df['transformation'][i]) 

    if method == "Lemmatization":
        if stop_choice == 'Remove':
            df["comment_no_Stopwords"] = df["comment_body"].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
            df["transformation"] = df["comment_no_Stopwords"].apply(lambda x: [wl.lemmatize(y) for y in x])
        else:
            df["transformation"] = df["comment_body"].apply(lambda x: [wl.lemmatize(y) for y in x])
        for i in df['transformation'].index:
            df['transformation'][i] = ''.join(df['transformation'][i])

    return df


def summary(df):
    num_comments = len(df[df['transformation'] != ''])
    num_user = len(list(set(df['username'])))
    
    num_hashtag = 0
    num_token = 0
    for i in range(len(df['transformation'])):
        for word in df['transformation'][i].split():
            if word[0] == '#':
                num_hashtag += 1
            num_token += 1
    return "In the uploaded dataset, "  + str(num_user) + " users contributed " + str(num_comments) + " comments. \nIn those comments, there are " + str(num_hashtag) +" hashtags and " + str(num_token) + " different tokens."


def calc_num(community_dict):
    for key in community_dict.keys():
        community_dict[key]['tokens_num'] = len(list(set(community_dict[key]['token'])))
        community_dict[key]['new_users'] = len(list(set(community_dict[key]['user_id'])))
        community_dict[key]['comments_num'] = len(community_dict[key]['user_id'])
            
def week_number(str1,str2):
    curr_date1 = str1.split('-')
    curr_date2 = str2.split('-')
    
    
    date1 = date(int(curr_date1[0]),int(curr_date1[1]),int(curr_date1[2][0:2]))
    date2 = date(int(curr_date2[0]),int(curr_date2[1]),int(curr_date2[2][0:2]))
    days = abs(date1-date2).days
    return days//7

def merge_list(sorted_list):
    prev_token = ""
    prev_date = ""
    prev_week = 0
    prev_use = 0
    new_list = []
    
    i = 0
    while i<len(sorted_list):
        while i<len(sorted_list) and sorted_list[i]['Token'] == prev_token and sorted_list[i]["Date"] == prev_date: 
            prev_use += sorted_list[i]['Use']
            i+=1
        
        new_dict = {}
        new_dict['Token'] = prev_token
        new_dict['Date'] = prev_date
        new_dict['Project_Week'] = prev_week
        new_dict['Use'] = prev_use
        
        if len(new_list)>0 and new_dict['Token'] == new_list[-1]['Token']:
            new_dict['Culmulative Use'] = new_dict['Use'] + new_list[-1]['Culmulative Use']
        else:
            new_dict['Culmulative Use'] = new_dict['Use']
         
        new_list.append(new_dict)
            
        prev_token = sorted_list[i]['Token']
        prev_date = sorted_list[i]['Date']
        prev_week = sorted_list[i]['Project_Week']
        prev_use = sorted_list[i]['Use']
        
        i+=1
        
    return new_list[1:]

def get_token_evolve(period, transformed):
    token_evolve_list = []
    first_appear_dict = {}

    for i in transformed['transformation'].index: 
        sentence = transformed['transformation'][i]
        sentence = re.sub(r'http\S+', '', sentence, flags=re.MULTILINE)
        tokens = sentence.split();
        try:
            current_date = transformed['comment_created_at'][i][:10]
        except:
            continue

        token_dict = {}
        for j in range(len(tokens)):
            curr_token = tokens[j]
            token_dict[curr_token] = {}
            if curr_token not in first_appear_dict:
                first_appear_dict[curr_token] = current_date
                num_proj_week = 0
            else:
                first_appear_week = first_appear_dict[curr_token]
                num_proj_week = week_number(current_date, first_appear_week)

            if "num_use" not in token_dict[curr_token]:
                token_dict[curr_token]['num_use'] = 1
            else:
                token_dict[curr_token]['num_use'] += 1

            token_dict[curr_token]['week_num'] = num_proj_week

        for key in token_dict.keys():
            curr_dict = {}
            curr_dict['Token'] = key
            curr_dict['Date'] = current_date
            curr_dict['Project_Week'] = token_dict[key]['week_num']
            curr_dict['Use'] = token_dict[key]['num_use']

            token_evolve_list.append(curr_dict)

    sorted_list = sorted(token_evolve_list, key=lambda d: d['Token'])
    new_list = merge_list(sorted_list)
    df = pd.DataFrame(new_list)
  
    return df

def generate_dict(df, community_dict):
    for i in range(len(df['comment_created_at'])):
        first_date = df['comment_created_at'][0]
        now_date = df['comment_created_at'][i]
        try:
            interval = week_number(now_date, first_date)
        except:
            if i == len(df['comment_created_at'])-1:
                calc_num(community_dict)
            else: 
                continue
        name_interval = 'W' + str(interval+1)
        if name_interval not in community_dict:
            community_dict[name_interval] = {}
            community_dict[name_interval]['tokens_num'] = 0
            community_dict[name_interval]['new_users'] = 0
            community_dict[name_interval]['comments_num'] = 0
            community_dict[name_interval]['token'] = []
            community_dict[name_interval]['user_id'] = []
            
        community_dict[name_interval]['token'].extend(list(set(df["transformation"][i].split())))
        community_dict[name_interval]['user_id'].append(str(df['username'][i]))
        
        if i == len(df['comment_created_at'])-1:
            calc_num(community_dict)
