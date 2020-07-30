# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 13:08:38 2020

@author: Lajari
"""

import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator
from re import search

import nltk
nltk.download('stopwords')
nltk.download('wordnet')

from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english')) 

class CleanDescriptionFile(TransformerMixin, BaseEstimator):
    '''This subclass is used to cleaning the data in description file'''
    
    def __init__(self, check_ASIN = True, add_category = True):
        self.check_ASIN = check_ASIN
        self.add_category = add_category
        

    def fit(self, X, y=None):
        return self
    
    
    def check_ASIN_validity(self,X):
        """ This fuction checks valid ASIN.
        ASIN : ASIN is unique identifier defined by amazon 
        for each productI"""
      
        if self.check_ASIN == True:
            col = X['ASIN'].copy()
            uniq_col = pd.Series(col.unique())
            mask = (uniq_col.str.match(r'\b[B\d][\dA-Z]{9}\b')) & (uniq_col.str.len()==10)
            inval_ASIN = uniq_col[~mask]
            print(inval_ASIN)
            return inval_ASIN

        
    
    def transform(self,X):
        """ Transformation includes cleaning inappropriate column and casting to appropriate format"""
        
        X =X[~X.duplicated(keep='first')].copy()
        X['Keyword'] = X['Keyword'].astype(str).str.replace('+',' ').str.replace('%27',"'").copy()
        X['MatchTerm'] = X['MatchTerm'].astype(str).str.replace('%27',"''").copy()
        X = X.fillna('Not Available').copy()
        X['RetrievedTime'] = pd.to_datetime(X['RetrievedTime']).copy()
        X = X[~(X['ProductName'] == 'No_Name')]

        X.rename(columns={"TotalCustRatings": "TotalCustomerRatings"}, inplace=True)
        X['ExclusionInProduct'] = X['ExclusionInProduct'].astype('int')
        X['IngredientInProduct'] = X['IngredientInProduct'].astype('int')
        X['KeywordDept'] =X['KeywordDept'].astype('int')
        X['TotalCustomerRatings'] = X['TotalCustomerRatings'].apply(lambda x: x.replace(',','')).astype('int')
        X['ProductStar'] = X['ProductStar'].astype('float')
        
        def classify(row):
            if search(r"[tT][eE][aA]|Traditional Medicinals Nighty Night Valerian,",row):
                return 'tea'
            elif search(r"[cC][oO][fF][fF][eE][eE]", row):
                return 'coffee'
            elif search(r"[cC][aA][pP][sS][uU][lL]|[Tt][aA][bB][lL][eE][tT]",row):
                return 'tablet'
            elif search(r"[cC][hH][oO][cC][oO][lL][aA][tT]",row):
                return 'chocolate'
            elif search(r"[oO][iI][lL]",row):
                return 'oil'
            elif search(r"[cC][oO][oO][kK][iI]",row):
                return 'cookies'
            elif search(r"[hH][oO][nN][eE][yY]",row):
                return 'honey'
            elif search(r"[Mm][iI][lL][kK]",row):
                return 'milk'   
            elif search(r"[jJ][aA][mM]|[jJ][eE][lL][lL][yY]",row):
                return 'jam'
            elif search(r"[Bb][eE][Vv][Ee][rR][aA][gG][eE]",row):
                return 'beverage'
            elif search(r"[Cc][aA][kK][eE]",row):
                return 'cake mix'
            elif search(r"[Ee][xX][tT][rR][Aa][cC][tT]",row):
                return 'extract'
            elif search(r"[sS][uU][pP][pP][lL][eE][mM][eE][nN][tT]",row):
                return 'supplement'
            elif search(r"[rR][oO][oO][tT]",row):
                return 'root'
            elif search(r"[lL][eE][aA][fFvV][eE]?",row):
                return 'leaf'
            elif search(r"[pP][oO][wW][dD][eE][rR]",row):
                return 'powder'
            else:
                return 'other'
            
        if self.add_category:          
            X['Category'] = X['ProductName'].map(classify)
        
        
        return X
    
class CleanReviewFile(TransformerMixin, BaseEstimator):
    '''This subclass is used to cleaning the data in review file'''
    
    def __init__(self, check_ASIN = True, add_ProcessedText = True):
        self.check_ASIN = check_ASIN
        self.add_ProcessedText = add_ProcessedText
        

    def fit(self, X, y=None):
        return self
    
    
    def check_ASIN_validity(self,X,y=None):
        """ This fuction checks valid ASIN.
        ASIN : ASIN is unique identifier defined by amazon 
        for each productI"""
        
        
        if self.check_ASIN == True:
            col = X['ASIN'].copy()
            uniq_col = pd.Series(col.unique())
            mask = (uniq_col.str.match(r'\b[B\d][\dA-Z]{9}\b')) & (uniq_col.str.len()==10)
            inval_ASIN = uniq_col[~mask]
            print(inval_ASIN)
            return inval_ASIN
    
    def transform(self,X,y=None):
        """ Transformation includes cleaning inappropriate column and casting to appropriate format"""
        
        X =X[~X.duplicated(keep='first')].copy()
        X['ProductNumReviews'] = X['ProductNumReviews'].astype(str).str.replace(',','').astype('int64')
        X['RetrievedTime'] = pd.to_datetime(X['RetrievedTime'])
        X['ReviewHelpful'] = X['ReviewHelpful'].astype(str).str.replace(',','').astype('int64')
        X = X.fillna({'ReviewersName':'Not Available', 'ReviewContent':'Not Available'})
        X = X[~(X['ProductName'] == 'No_Name')]

        X['ReviewEarly'] = X['ReviewEarly'].astype('int')
        X['ReviewStar'] = X['ReviewStar'].astype('float')
        X['ReviewTime'] = X(df_reviews['ReviewTime'])
        X['ReviewVerifiedP'] = X['ReviewVerifiedP'].astype('int')
        X['ReviewVine'] = X['ReviewVine'].astype('int')

        
        def cleanreview(t):
            t = t.lower()
            t = RegexpTokenizer(r'[a-zA-Z]+').tokenize(t)
            t = [x for x in t if x not in stop_words]
            t = [lemmatizer.lemmatize(x, pos = "v") for x in t ]
            t = " ".join(t)
            return t
            
        if self.add_ProcessedText == True:
            X['ProcessedText'] = X['ReviewContent'].map(cleanreview)
   
        return X
    
