
import os
from beartype import beartype
import numpy as np
import pandas as pd
from adi_parse import AdiParse
import search_function
from get_all_comments import GetComments

@beartype
def get_file_data(folder_path:str, channel_structures:dict):
    """
    Get file data in dataframe

    Parameters
    ----------
    folder_path : str
    channel_structures : dict, keys =  total channels, values = channel list

    Returns
    -------
    file_data : pd.DataFrame

    """
    
    # get file list
    filelist = list(filter(lambda k: '.adicht' in k, os.listdir(folder_path)))

    for i, file in enumerate(filelist): # iterate over list
    
        # initiate adi parse object      
        adi_parse = AdiParse(os.path.join(folder_path, file), channel_structures)
        
        # get all file data in dataframe
        temp_file_data = adi_parse.get_all_file_properties()
        
        # add folder path
        temp_file_data['folder_path'] = folder_path 
        
        if i == 0:
            file_data = temp_file_data         
        else:  
            file_data = file_data.append(temp_file_data, ignore_index = True)
            
    # convert data frame to lower case
    file_data = file_data.apply(lambda x: x.astype(str).str.lower())
    
    # convert file length to int
    file_data['file_length'] = file_data['file_length'].astype(np.int64)
    
    return file_data


def get_channel_structures(user_data):
    """
    Get channel structure from SAKE user data

    Parameters
    ----------
    user_data : Dataframe with user data for SAKE input

    Returns
    -------
    order : List with channels in order

    """
    
    
    # define separator
    separtor = '-'
    
    # get data containing channel order
    channel_structures = user_data[user_data['Source'] == 'total_channels']
    
    regions = {}
    for i in range(len(channel_structures)):
        
        # retrieve channel names
        channel_names = channel_structures['Assigned Group Name'][i]
        
        # get list of channels for each total channels entry
        region_list = channel_names.split(separtor)
        regions.update({int(channel_structures['Search Value'][i]): region_list})
        
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
        idx = getattr(search_function, user_data.at[i, 'Search Function'])(file_data[source], user_data.at[i, 'Search Value'])                              
        
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
    warning_str: str, string used for warning
    """
    
    # create empty dataframes for storage
    logic_index_df = pd.DataFrame()
    index_df = pd.DataFrame()
    warning_str = ''
    
    # create sources list
    sources = ['channel_name', 'file_name']
    
    for source in sources: # iterate over user data entries  
        
        # find which groups exist in which files in each source
        df = get_source_logic(file_data, user_data, source)
        
        # concatenate with index
        logic_index_df = pd.concat([logic_index_df, df], axis=1)
            
    # add columns from file to data
    add_columns = ['folder_path','file_name','file_length', 'channel_id', 'block' , 'sampling_rate', 'brain_region',]
    index_df = pd.concat([index_df, file_data[add_columns]], axis=1)
    
    # get time
    index_df['start_time'] = 0
    index_df['stop_time'] = file_data['file_length']
        
    # get category with group names
    groups_ids = get_categories(user_data)
    
    # convert logic to groups
    index_df = convert_logicdf_to_groups(index_df, logic_index_df, groups_ids)
    
    # get time and comments
    obj = GetComments(file_data, user_data, 'comment_text', 'comment_time')
    index_df, com_warning = obj.add_comments_to_index(index_df)
    
    # reset index and rename previous index to file_id
    index_df = index_df.rename_axis('file_id').reset_index()
    
    # check if groups were not detected
    if index_df.isnull().values.any():
        # breakpoint()
        # nan_cols = str(list(index_df.columns[index_df.isna().any()]))
        warning_str = 'Some conditons were not found!'
        # index_df = index_df.replace(np.nan, 'not_found', regex=True)
        # raise Exception('Some conditons were not detected in the following column(s): ' + nan_cols)
    
    # check if user selected time exceeds bounds
    if (index_df['start_time']<0).any() or (index_df['start_time']>index_df['file_length']).any():
        raise Exception('Start time exceeds bounds.')
    elif (index_df['stop_time']<0).any() or (index_df['stop_time']>index_df['file_length']).any():
        raise Exception('Stop time exceeds bounds.')
    
    # get added group names based on user input
    group_columns = list(index_df.columns[index_df.columns.get_loc('stop_time')+1:]) + ['brain_region']
    
    # put categories at end
    index_df = index_df[ [x for x in list(index_df.columns) if x not in group_columns] + group_columns]           
    return index_df, group_columns, warning_str + com_warning


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
    warning_str: str, string used for warning

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
    channel_structures = get_channel_structures(user_data)
    
    # get all file data in dataframe
    file_data = get_file_data(folder_path, channel_structures)
    
    # get index datframe
    index_df, group_columns, warning_str = create_index_array(file_data, user_data)
    
    return index_df, group_columns, warning_str

if __name__ == '__main__':
    
    
    # define path
    folder_path = r'C:\Users\panton01\Desktop\example_files'
    
    # get user table data example
    user_data = pd.read_csv(r'C:\Users\panton01\Desktop\user_data - Copy.csv')
    
    # convert data frame to lower case
    user_data = user_data.apply(lambda x: x.astype(str).str.lower())
    
    # remove rows with no source
    user_data = user_data[user_data.Source != '']
    
    # get channel order
    channel_structures = get_channel_structures(user_data)
    
    # get all file data in dataframe
    file_data = get_file_data(folder_path, channel_structures)

    # get experiment index
    index_df, group_columns, warning_str = create_index_array(file_data, user_data)
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    