
import os
from beartype import beartype
import numpy as np
import pandas as pd
from adi_parse import AdiParse
import string_filters
from get_comments import GetComments

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


def get_channel_order(user_data):
    """
    Get channel order from user data

    Parameters
    ----------
    user_data : Dataframe with user data

    Returns
    -------
    order : List with channels in order

    """
    
    # get data containing channel order
    channel_order = user_data[user_data['Source'] == 'channel_order']
    
    # sort by order number
    channel_order = channel_order.sort_values(by=['Search Value'])
    
    # get order and channel names in 
    order = list(channel_order['Search Value'])
    regions = list(channel_order['Assigned Group Name'])
    
    # find integers
    integers = [s for s in order if s.isdigit()]
    
    if len(order) != len(integers):
        raise Exception('Channel order option accepts only integers. e.g.: 1,2,3')
        
    if len(order) != len(regions):
        raise Exception('Each group name requires an order number')
        
    if len(set(order)) != len(order):
        raise Exception('Each number in channel order must be unique. Got:', order, 'instead')
        
    return regions


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
    Reverse hot coding in dataframe and replace with column names or nan
    

    Parameters
    ----------
    sort_df : pd.DataFrame, with columns in one hot encoding format

    Returns
    -------
    col_labels: 1D np.array with columns retrieved from one hot encoded format

    """

    # get columns
    labels = np.array(sort_df.columns)
    
    # find index where column is True #np.argmax(np.array(sort_df), axis = 1)
    idx_array = np.array(sort_df)
    col_labels = np.zeros(len(sort_df), dtype=object)
    
    for i in range(idx_array.shape[0]): # iterate over idx_array
        
        # find which column
        idx = np.where(idx_array[i] == True)[0]
        
        if len(idx) == 0:       # if no True value present
            col_labels[i] = np.NaN
        elif  len(idx) > 1:     # if more than one True value present
            col_labels[i] = np.NaN
        elif len(idx) == 1:     # if one True value present
            col_labels[i] = labels[idx[0]]
            
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

    
def get_source_logic(file_data, user_data, source:str):
    """
    Find which unique groups exist and return as dataframe

    Parameters
    ----------
    user_data : pd.DataFrame
    source : str, source destination

    Returns
    -------
    index : pd.DataFrame

    """
    
    # get only user data form source
    user_data = user_data[user_data['Source'] == source].reset_index()
    
    index = {}
    for i in range(len(user_data)): # iterate over user data entries       
                
        # find index for specified source and match string
        idx = getattr(string_filters, user_data.at[i, 'Search Function'])(file_data[source], user_data.at[i, 'Search Value'])                              
        
        # append to index dictionary                
        index.update({user_data.at[i, 'Assigned Group Name']: idx})
        
    return pd.DataFrame(index)
    
    

def create_index_array(file_data, user_data):
    """
    Create index for experiments according to user selection

    Parameters
    ----------
    file_data : pd.DataFrame, aggregated data from labchart files
    user_data : pd.DataFrame, user search and grouping parameters

    Returns
    -------
    index_df: pd.DataFrame, with index
    group_columns: list, column names that denote groups
    """
    
    # create empty dataframes for storage
    logic_index_df = pd.DataFrame()
    index_df = pd.DataFrame()
    
    # create sources list
    sources = ['channel_name', 'file_name']
    
    for source in sources: # iterate over user data entries  
        
        # find which groups exist in which files in each source
        df = get_source_logic(file_data, user_data, source)
        
        # concatenate with index
        logic_index_df = pd.concat([logic_index_df, df], axis=1)
            
    # add columns from file to data
    add_columns = ['file_name', 'channel_id', 'block' , 'sampling_rate', 'brain_region']
    index_df = pd.concat([index_df, file_data[add_columns]], axis=1)
    
    # get time
    index_df['start_time'] = 0
    index_df['stop_time'] = file_data['file_length']
        
    # get category with group names
    groups_ids = get_categories(user_data)
    
    # convert logic to groups
    index_df = convert_logicdf_to_groups(index_df, logic_index_df, groups_ids)
    
    # get time and comments ( # check when no comments are present)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    obj = GetComments(file_data, user_data, 'comment_text', 'comment_time')
    index_df = obj.add_comments_to_index(index_df)
    
    # check if groups were not detected
    if index_df.isnull().values.any():
        nan_cols = str(list(index_df.columns[index_df.isna().any()]))
        raise Exception('Some conditons were not detected in the following column(s): ' + nan_cols)
    
    # get added group names based on user input
    group_columns = list(index_df.columns[index_df.columns.get_loc('stop_time')+1:]) + ['brain_region']
                     
    return index_df, group_columns


def get_index_array(folder_path, user_data):
    """
    Get file data, channel array and create index
    for experiments according to user selection

    Parameters
    ----------
    file_data : pd.DataFrame, aggregated data from labchart files
    user_data : 2D list, user search and grouping parameters from datatable

    Returns
    -------
    index_df: pd.DataFrame, with index
    group_columns: list, column names that denote groups

    """
    
    # get dataframe and convert to lower case
    user_data = pd.DataFrame(user_data)
    user_data = user_data.apply(lambda x: x.astype(str).str.lower())
        
    # remove rows with missing inputs
    user_data = user_data.dropna(axis = 0)
    
    # ensure group names are unique
    if len(user_data['Assigned Group Name']) != len(user_data['Assigned Group Name'].unique()):
        raise Exception('Duplicate -Assigned Group Names- were found. Please check that -Assigned Group Names- are unique')
    
    # get channel order
    channel_order = get_channel_order(user_data)
    
    # get all file data in dataframe
    file_data = get_file_data(folder_path, channel_order)
    
    # get index datframe
    index_df, group_columns = create_index_array(file_data, user_data)
    
    return index_df, group_columns

if __name__ == '__main__':
    
    
    # define path
    folder_path = r'C:\Users\panton01\Desktop\example_files'
    
    # get user table data example
    user_data = pd.read_csv('example_data/default_table_data.csv')
    
    # convert data frame to lower case
    user_data = user_data.apply(lambda x: x.astype(str).str.lower())
    
    # remove rows with no source
    user_data = user_data[user_data.Source != '']
    
    # get channel order
    channel_order = get_channel_order(user_data)
    
    # get all file data in dataframe
    file_data = get_file_data(folder_path, channel_order)

    # get experiment index
    index_df, group_columns = create_index_array(file_data, user_data)
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    