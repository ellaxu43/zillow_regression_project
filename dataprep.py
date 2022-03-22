import os
import pandas as pd
import env
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

from env import user, password, host


database_url_base = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/'


def get_zillow_data(use_cache=True):
    if os.path.exists('zillow.csv') and use_cache:
        print('Using cached csv')
        df = pd.read_csv('zillow.csv')
        df = df.rename(columns = {'bedroomcnt':'bedrooms', 
                              'bathroomcnt':'bathrooms', 
                              'calculatedfinishedsquarefeet':'area',
                              'taxvaluedollarcnt':'tax_value', 
                              'yearbuilt':'year_built'})
        return df
    
    
    print('Acquiring data from SQL database')
    query = '''
    SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    FROM properties_2017

    LEFT JOIN propertylandusetype USING(propertylandusetypeid)

    WHERE propertylandusedesc IN ("Single Family Residential",                       
                                  "Inferred Single Family Residential")

    '''
    df = pd.read_sql(query, database_url_base + 'zillow')
    df = df.rename(columns = {'bedroomcnt':'bedrooms', 
                              'bathroomcnt':'bathrooms', 
                              'calculatedfinishedsquarefeet':'area',
                              'taxvaluedollarcnt':'tax_value', 
                              'yearbuilt':'year_built'})
    df.to_csv('zillow.csv', index=False)
   
    return df


def remove_outliers(df, k, col_list):
    ''' remove outliers from a list of columns in a dataframe 
        and return that dataframe
    '''
    
    for col in col_list:

        q1, q3 = df[col].quantile([.25, .75])  # get quartiles
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # return dataframe without outliers
        
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        
    return df


def prepare_zillow(df):
        # Prepare zillow data for exploration'''

    # removing outliers
        df = remove_outliers(df, 1.5, ['bedrooms', 'bathrooms', 'area', 'tax_value', 'taxamount'])
    
    # converting column datatypes
        df.fips = df.fips.astype(object)
        df.year_built = df.year_built.astype(object)
    
    # train/validate/test split
        train_validate, test = train_test_split(df, test_size=.2, random_state=123)
        train, validate = train_test_split(train_validate, test_size=.3, random_state=123)
    
    # impute year built using mode
        imputer = SimpleImputer(strategy='median')

        imputer.fit(train[['year_built']])

        train[['year_built']] = imputer.transform(train[['year_built']])
        validate[['year_built']] = imputer.transform(validate[['year_built']])
        test[['year_built']] = imputer.transform(test[['year_built']])       
    
        return train, validate, test    


def wrangle_zillow():
    '''Acquire and prepare data from Zillow database for explore'''
    train, validate, test = prepare_zillow(get_zillow_data())
    
    return train, validate, test

