
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


def get_categories(user_data):
    """
    Get unique categories and groups in dictionary.

    Parameters
    ----------
    user_data : pd.DataFrame, with user group inputs.

    Returns
    -------
    groups : dict, keys are unique categories and groups.
    
    """
    
    # get unique categories
    unique_categories = user_data['Category'].unique()
    
    groups = {} # create group dictionary
    for category in unique_categories: # iterate over categories
        
        # which groups exist in categories
        groups.update({category: list(user_data['Assigned Group Name'][user_data['Category'] == category]) })
        
    return groups


def reverse_hot_encoding(sort_df):
    """
    Reverse hot coding in dataframe and replace with

    Parameters
    ----------
    sort_df : pd.DataFrame, with columns in one hot encoding format

    Returns
    -------
    col_labels: 1D np.array with columns retrieved from one hot encoded format

    """

    # get columns
    labels = np.array(sort_df.columns)
    
    # find index where column is True
    idx = np.argmax(np.array(sort_df), axis = 1)
    
    # map columns to index
    col_labels = np.array(list(map(labels.item, idx)))  
    
    return col_labels
    

def convert_logicdf_to_groups(index_df, logic_index_df, groups_ids:dict):
    """
    Convert logic from logic_index_df to groups and and append to index_df

    Parameters
    ----------
    index_df : pd.DataFrame, to append categories
    logic_index_df : pd.DataFrame, containing logic
    groups_ids : dict, containg categories as keys and groups as values

    Returns
    -------
    index_df : pd.DataFrame

    """
    
    # convert logic to groups
    for category, groups in groups_ids.items():
        
        # check if all groups present in dataframe
        groups_present = all(elem in logic_index_df.columns  for elem in groups)
        
        if (groups_present == True): # are all groups present in dataframe?
            if (logic_index_df[groups].any().any() == True):  # was any group detected? 
            
                # convert logic to groups
                index_df[category] = reverse_hot_encoding(logic_index_df[groups])
                
    return index_df
    
    
    

def add_comments_to_index(file_data, user_data, fs = 4000):
    
    # string to fetch columns
    comment_text = 'comment_text'
    comment_time = 'comment_time'
    
    # get file data column names
    comment_text_cols = list(file_data.columns[file_data.columns.str.contains(comment_text)])
    comment_time_cols = list(file_data.columns[file_data.columns.str.contains(comment_time)])
    com = dict(zip(comment_text_cols, comment_time_cols))
    
    # get user data containing comment text
    user_com_text = user_data[user_data['Source'] == comment_text].reset_index()
    
    # create empty arrays
    index = {}
    index_text = {} # create empty dictionary to store index from search
    index_time = {} # create empty dictionary to store time for each comment
    
    for i in range(len(user_com_text)): # user comment groups
    
        for comtext,comtime in com.items(): # file comments
                
            # find index for specified source and match string
            idx = getattr(string_filters, user_com_text.at[i, 'Search Function'])(file_data[comtext], user_com_text.at[i, 'Search Value'])
            
            index_text.update({comtext:idx})
            index_time.update({comtime:file_data[comtime]})
            
        # create dataframe
        com_text_df = pd.DataFrame(index_text) 
        com_time_array = np.array(pd.DataFrame(index_time))
        if np.any(np.all(com_text_df,axis=1)) == True:
            print('more than one comment present')
        else:
            
            # get comment times
            user_time = user_com_text.at[i, 'Time Selection (min)'].split(':')
            user_time = np.array([int(x) for x in user_time])* fs*60
            
            # get comment index
            com_idx = np.argmax(np.array(com_text_df), axis = 1)
            idx = np.zeros((com_idx.shape[0],2))
            
            for ii in range(len(com_text_df)):
                
                # get index of where comment was detected
                idx_one = np.where(com_text_df.iloc[ii,:] == True)[0]
                               
                if len(idx_one) == 0: # if no comment was detected
                    idx[ii] = file_data['file_length'][ii]
                else:
                    idx[ii,:] = int(float(com_time_array[ii,idx_one[0]])) + user_time
                               
            # add comment to index
            index.update({user_data.at[i, 'Assigned Group Name']: idx})
            
    
    # for i in len(com_text_df):
        
        # com_text_df.at[i,'time'] = com_time_array[np.array(com_text_df)]
    
    # #
        
    
    return com_text_df
     
        
             

def create_index_array(file_data, user_data):
    """
    Create boolean index array for each search value

    Parameters
    ----------
    file_data : pd.DataFrame, aggregated data from labchart files
    user_data : pd.DataFrame, user search and grouping parameters

    Returns
    -------
    index_df: pd.DataFrame, with index

    """
    

    # create sources list
    sources = ['channel_name', 'file_name']
    
    index = {} # create empty dictionary to store index from search
    
    for i in range(len(user_data)): # iterate over user data entries       
        for source in sources: # iterate over source types    

            if user_data.at[i, 'Source'] in source: # check if source matches user data
                
                # find index for specified source and match string
                idx = getattr(string_filters, user_data.at[i, 'Search Function'])(file_data[source], user_data.at[i, 'Search Value'])                              
                
                # append to index dictionary                
                index.update({user_data.at[i, 'Assigned Group Name']: idx}) 
    
    
    # convert to dataframe
    logic_index_df = pd.DataFrame(index)
    
    # create empty dataframe for index
    index_df = pd.DataFrame()
               
    # add columns
    add_columns = ['file_name', 'channel_id', 'block' ,'brain_region',  'file_length']
    for col in add_columns:
        index_df[col] = file_data[col]   
        
    # get category with group names
    groups_ids = get_categories(user_data)
    
    # convert logic to groups
    index_df = convert_logicdf_to_groups(index_df, logic_index_df, groups_ids)
                         
    return index_df
            


        

if __name__ == '__main__':
    
    
    # define path
    folder_path = r'C:\Users\panton01\Desktop\example_files'
    
    # get user table data example
    user_data = pd.read_csv('example_data/default_table_data.csv')
    # convert data frame to lower case
    user_data = user_data.apply(lambda x: x.astype(str).str.lower())
    # remove rows with no source
    user_data = user_data[user_data.Source != '']
    
    # check that assigned group name is unique
    
    
    # get channel order
    channel_order = string_filters.get_channel_order(user_data)
    
    # get all file data in dataframe
    file_data = get_file_data(folder_path, channel_order)
    
    index_df = create_index_array(file_data, user_data)
    
    # comdf = add_comments_to_index(file_data, user_data)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    