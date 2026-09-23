import requests
import json
import pandas as pd
import spacy
import re
import os

API_KEY = os.environ.get("NEWS_API_KEY")

nlp = spacy.load("en_core_web_sm")

keyword_drop_list = []
current_articles = None

def keyword_filter(keywords):

    for word in keywords:
        if word in keyword_drop_list:
            print("WORD FOUND IN FILTER:", word)
            keywords.remove(word)

    return keywords



def create_keyword_list(df_staging):

    print("CREATE_KEYWORD_LIST 'START'")

    pos_type = ["PROPN","NOUN","VERB"]

    df_length = len(df_staging)

    num = 0

    
    while num < df_length:
        #title = df_staging['title'][num]
        title = df_staging.at[num,'title']
        doc = nlp(title)

        keyword_list = []

        if pd.notna(title):
            #print("TITLE NOT NA:", title)

            for word in doc:
                #print(word)
                for pos in pos_type:
                    if word.pos_ == pos:

                        if len(str(word)) < 3:
                            if str(word).isalnum() == True:
                                keyword_list.append(str(word))
                        else:
                            keyword_list.append(str(word))

        #print("BEFORE FILTERING",keyword_list)
        #keyword_list = keyword_filter(keyword_list)

        #df_staging["Keywords"][num] = keyword_list
        df_staging.at[num,"Keywords"] = keyword_list

        print("NEW KEYWORD LIST FOR TABLE:",df_staging["Keywords"][num])


        num = num + 1

    print("DATAFRAME RETURNED")
    return df_staging


def filter_articles(df):

    filtered_df = df.copy();

    for keyword in keyword_drop_list:
        filtered_df = filtered_df[
            ~filtered_df["Keywords"].apply(
                lambda keywords: keyword in keywords
            )
        ]

    return filtered_df



def get_news(selected_date, selected_category, selected_sources, input_keywords):

    global current_articles

    if selected_sources == "Any":
       url = ( 'https://newsapi.org/v2/top-headlines?' +
                #  'sources=' + selected_sources + '&' +
                   'country=us&' +
                   'q=' + input_keywords + '&' +
                   'category=' + selected_category + '&' +
                   'from=' + selected_date + '&' +
                   'sortBy=popularity&' +
                   'apiKey=' + API_KEY
               ) 
    else:
        url = ( 'https://newsapi.org/v2/top-headlines?' +
                'sources=' + selected_sources + '&' +
                'country=us&' +
                'q=' + input_keywords + '&' +
                'category=' + selected_category + '&' +
                'from=' + selected_date + '&' +
                'sortBy=popularity&' +
                'apiKey=' + API_KEY
            )


    # Making the dataframe
    response = requests.get(url)
    
    data = response.json()
    
    df = pd.json_normalize(data['articles'])
    
    df_staging = df.filter(items = ['title', 'author', 'description', 'country', 'publishedAt', 'content', 'source.name', 'url'], axis=1)
    df_staging = df_staging.drop_duplicates()
    
    df_staging["Keywords"] = pd.NA

    create_keyword_list(df_staging)

    current_articles = df_staging

    return filter_articles(current_articles)


def droplist_add(keyword_input):

    global keyword_drop_list
        
    user_add = keyword_input
    user_add = re.sub(r"\W", " ", user_add)
        
    for i in user_add.split():
        if i not in keyword_drop_list:
            keyword_drop_list.append(i)
        else: 
            print("keyword already added to keyword_drop_list")
    
    print("KEYWORD LIST AFTER ADDING:",keyword_drop_list)


def droplist_remove(keyword_input):

    global keyword_drop_list

    print("KEYWORD LIST BEFORE CHANGES:", keyword_drop_list)
    print("KEYWORD X'd: ", repr(keyword_input))

    user_drop = keyword_input
    user_drop = re.sub(r"\W", " ", user_drop)
    
    
    for i in user_drop.split():
        if i not in keyword_drop_list:
            print("Keyword Not Found")
        else:
            keyword_drop_list.remove(i)
            
    print("KEYWORD LIST AFTER CHANGE:",keyword_drop_list)


def get_droplist(input_keyword_add, input_keyword_drop):
    
    droplist_add(input_keyword_add)
    droplist_remove(input_keyword_drop)

   
    return keyword_drop_list


def get_filtered_articles():

    print("CURRENT ARTICLES:")
    print(current_articles)

    print("DROP LIST:")
    print(keyword_drop_list)

    filtered_articles = filter_articles(current_articles)

    print("FILTERED ARTICLES:")
    print(filtered_articles)

    return filtered_articles
