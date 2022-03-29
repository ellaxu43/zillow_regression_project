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
          
SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, 
taxvaluedollarcnt, yearbuilt, fips
FROM properties_2017 
JOIN propertylandusetype  
ON properties_2017.propertylandusetypeid = propertylandusetype.propertylandusetypeid
AND propertylandusedesc 
IN ("Single Family Residential",                       
 "Inferred Single Family Residential")
JOIN predictions_2017 USING(parcelid)
where predictions_2017.transactiondate LIKE '2017%%';
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
        df = remove_outliers(df, 1.5, ['bedrooms', 'bathrooms', 'area', 'tax_value'])
        
    #replace 1.75 bathrooms to 2 bathrooms. 
        df['bathrooms'] = df['bathrooms'].replace({1.75 : 2})
    
    
    # impute year built using mode
        imputer = SimpleImputer(strategy='median')

        imputer.fit(df[['year_built']])
        
        df[['year_built']] = imputer.transform(df[['year_built']])
    
    # create feature engineering home_age 
        df['home_age'] = (2017 - df['year_built'])

    
    # converting column datatypes
        df.fips = df.fips.astype(object)
        df.year_built = df.year_built.astype(object)
        
        
        
    # create dummies for fips.   
        df['county'] = ""

        df.loc[(df.fips== 6037, 'county')] = "LA_county"

        df.loc[(df.fips== 6059, 'county')] = "orange_county"
          
        df.loc[(df.fips== 6111, 'county')] = "ventura_county"

        dummy_df = pd.get_dummies(df[['county']], dummy_na=False, \
                              drop_first=False)

        df = pd.concat([df, dummy_df], axis=1)
        
     #lastly, drop fips. 
        df = df.drop(columns = ['fips'])
    
    # train/validate/test split
        train_validate, test = train_test_split(df, test_size=.2, random_state=123)
        train, validate = train_test_split(train_validate, test_size=.3, random_state=123)
    
    # impute year built using mode
#         imputer = SimpleImputer(strategy='median')

#         imputer.fit(train[['year_built']])

#         train[['year_built']] = imputer.transform(train[['year_built']])
#         train['home_age'] = (2017 - train['year_built'])
#         validate[['year_built']] = imputer.transform(validate[['year_built']])
#         validate['home_age'] = (2017 - validate['year_built'])
#         test[['year_built']] = imputer.transform(test[['year_built']])       
#         test['home_age'] = (2017 - test['year_built'])
        
        return train, validate, test    


def wrangle_zillow():
    '''Acquire and prepare data from Zillow database for explore'''
    train, validate, test = prepare_zillow(get_zillow_data())
    
    return train, validate, test

