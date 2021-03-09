# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 20:48:19 2021

@author: Satyaki Ray
"""
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def load_msg():
    messages = pd.read_csv('messages.csv')
    categories = pd.read_csv('categories.csv')
    ## Merging Datasets
    df=pd.merge(messages,categories,how='inner',on='id')
    
    ## splitting categories
    categories = pd.DataFrame(df.categories.str.split(';').tolist())
    row = categories.iloc[0,:]
    category_colnames = row.apply(lambda x:x.split('-')[0])
    categories.columns = category_colnames
    
    ## Converting values to either 0 or 1
    for column in categories:
    # set each value to be the last character of the string
    categories[column] = categories[column].str[-1]
    # convert column from string to numeric
    categories[column] = categories[column].astype('int')
    
    # drop the original categories column from `df`
    df.drop('categories',axis=1,inplace=True)
    
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df,categories],axis=1)
    
    # drop duplicates
    df.drop_duplicates(inplace=True)
    
    engine = create_engine('sqlite:///DisasterResponse.db')
    df.to_sql('cleaned_msg', engine, index=False)
    
    
    

    