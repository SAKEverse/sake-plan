
import os
from beartype import beartype
import numpy as np
import pandas as pd
from adi_parse import AdiParse
import string_filters

@beartype
def get_file_data(folder_path:str, channel_order:list):
    """
    Get file data in dataframe

    Parameters
    ----------
    folder_path : str
    channel_order : list, with channel names in order

    Returns
    -------
    file_data : pd.DataFrame

    """
    
    # get file list
    filelist = list(filter(lambda k: '.adicht' in k, os.listdir(folder_path)))

    for i, file in enumerate(filelist): # iterate over list
    
        # initiate adi parse object      
        adi_parse= AdiParse(os.path.join(folder_path, file), channel_order)
        
        # get all file data in dataframe
        temp = adi_parse.get_all_file_properties()
        
        if i == 0:
            file_data = temp         
        else:  
            file_data = file_data.append(temp, ignore_index = True)
            
     
    # convert data frame to lower case
    file_data = file_data.apply(lambda x: x.astype(str).str.lower())
    
    return file_data
             

def create_index_array(file_data, user_data):
    """
    Create boolean index array for each search value

    Parameters
    ----------
    file_data : pd.DataFrame, aggregated data from labchart files
    user_data : pd.DataFrame, user search and grouping parameters

    Returns
    -------
    pd.DataFrame, with index

    """
    
    # create sources list
    sources = list(file_data.columns[file_data.columns.str.contains('comment_text')])
    sources.extend(['channel_name', 'file_name'])
    
    index = {} # create empty dictionary to store index from search
    
    for i in range(len(user_data)): # iterate over user data entries       
        for source in sources: # iterate over source types    

            if source in user_data.at[i, 'Source']: # check if source matches user data
                
                # find index for specified source and match string
                idx = getattr(string_filters, user_data.at[i, 'Search Function'])(file_data[source], user_data.at[i, 'Search Value'])
                index.update({user_data.at[i, 'Assigned Group Name']: idx}) # append to index dictionary
                         
    return pd.DataFrame(index)
            
            

if __name__ == '__main__':
    
    
    # define path
    folder_path = r'C:\Users\panton01\Desktop\example_files'
    
    # get user table data example
    user_data = pd.read_csv('example_data/default_table_data.csv')
    # convert data frame to lower case
    user_data = user_data.apply(lambda x: x.astype(str).str.lower())
    
    # get channel order
    channel_order = string_filters.get_channel_order(user_data)
    
    # get all file data in dataframe
    file_data = get_file_data(folder_path, channel_order)
    
    df = create_index_array(file_data, user_data)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    