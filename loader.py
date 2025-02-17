import os
import requests
import numpy as np
import pandas as pd

DATA_PATH = 'data/sample_dirty.csv'


# def download_data(url, force_download=False, ):
#     # Utility function to donwload data if it is not in disk
#     data_path = os.path.join('data', os.path.basename(url.split('?')[0]))
#     if not os.path.exists(data_path) or force_download:
#         # ensure data dir is created
#         os.makedirs('data', exist_ok=True)
#         # request data from url
#         response = requests.get(url, allow_redirects=True)
#         # save file
#         with open(data_path, "w") as f:
#             # Note the content of the response is in binary form: 
#             # it needs to be decoded.
#             # The response object also contains info about the encoding format
#             # which we use as argument for the decoding
#             f.write(response.content.decode(response.apparent_encoding))

    # return data_path


def load_formatted_data(data_fname:str) -> pd.DataFrame:
    """ One function to read csv into a dataframe with appropriate types/formats.
        Note: read only pertinent columns, ignore the others.
    """
    df = pd.read_csv(data_fname)
    df= df.astype(str)
    pd.to_numeric(df['lat_coor1'], errors='coerce').astype('float')
    pd.to_numeric(df['long_coor1'], errors='coerce').astype('float')
    pd.to_datetime(
    df.dermnt, 
    errors='coerce',
    format='%Y-%m-%d')
    
    return df


# once they are all done, call them in the general sanitizing function
def sanitize_data(df:pd.DataFrame) -> pd.DataFrame:
    """ One function to do all sanitizing"""
    have_dash = df.tel1 == '-'
    have_dash1 = df.adr_num == '-'
    have_dash2 = df.adr_voie == '-'
    has_zero = df.com_cp == '0'
    
    df.tel1[have_dash].isna()
    
    df.adr_num[have_dash].isna()
    
    df.adr_voie[have_dash].isna()
    
    df.com_cp[has_zero].isna()

    return df


# Define a framing function
def frame_data(df:pd.DataFrame) -> pd.DataFrame:
    """ One function all framing (column renaming, column merge)"""

    df['Adresse'] = df['adr_num'].astype(str) + " " + df['adr_voie'].astype(str) + ", " + df['com_cp'].astype(str) + ", " + df['com_nom'].astype(str)

    df=df.drop('adr_num',axis=1)
    df=df.drop('adr_voie',axis=1)
    df=df.drop('com_cp',axis=1)
    df=df.drop('com_nom',axis=1)


    return df


# once they are all done, call them in the general clean loading function
def load_clean_data(data_path:str=DATA_PATH)-> pd.DataFrame:
    """one function to run it all and return a clean dataframe"""
    df = (load_formatted_data(data_path)
          .pipe(sanitize_data)
          .pipe(frame_data)
    )
    return df


 # if the module is called, run the main loading function

df=load_clean_data(DATA_PATH)
print(df)