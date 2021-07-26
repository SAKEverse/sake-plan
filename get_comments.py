# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 10:59:45 2021

@author: panton01
"""

import numpy as np
import pandas as pd
import string_filters



class GetComments:
    """
    Get experiment index from user comments and groups
    """
    
    @staticmethod
    def get_index_file_com(com_logic_df, time_array, label):
        """
        Add Nans to comments not present and get respective time.
        
    
        Parameters
        ----------
        com_logic_df : pd.DataFrame
        time_array : pd.DataFrame
        label : str
        
    
        Returns
        -------
        com_label : nd array,
        com_time : nd array,
    
        """
    
       
        # find index where column is True
        idx_array = np.array(com_logic_df)
        com_label = np.zeros(len(com_logic_df), dtype = bool)
        com_time = np.zeros(len(com_logic_df))
        
        for i in range(idx_array.shape[0]): # iterate over idx_array
            
            # find which column
            idx = np.where(idx_array[i] == True)[0]
            
            if len(idx) == 0:       # if no True value present
                com_label[i] = False
                com_time[i] = np.NaN
            elif  len(idx) > 1:     # if more than one True value present
                com_label[i] = np.NaN
                com_time[i] = np.NaN
            elif len(idx) == 1:     # if one True value present
                com_label[i] = True
                com_time[i] = time_array.iloc[i, idx[0]]
    
        return com_label, com_time
    
    
    def __init__(self, file_data, user_data, comment_text:str, comment_time:str):
        """
        

        Parameters
        ----------
        file_data : pd.DataFrame, aggregated data from labchart files
        user_data : pd.DataFrame, user search and grouping parameters
        comment_text : str, to search file_data columns for comment text
        comment_time : str, to search file_data columns for comment times

        Returns
        -------
        None.

        """

        
        # pass to object
        self.comment_text = comment_text
        self.comment_time = comment_time

        # Get matching comment text and time columns from file_data dataframe
        self.com_text_cols = list(file_data.columns[file_data.columns.str.contains(self.comment_text)])
        self.com_time_cols = list(file_data.columns[file_data.columns.str.contains(self.comment_time)])
        self.com_match = dict(zip(self.com_text_cols, self.com_time_cols))
        
        # pass file data to object
        self.file_data = file_data    
        
        # get user data containing comment text
        self.user_data = user_data[user_data['Source'] == self.comment_text].reset_index()
        
        # get groups
        self.com_categories = list(self.user_data.Category.unique())
       
    
    def get_index_per_comment(self, index:int):
        """
        Get boolean index for comment. True if a comment is present. 
        Along with it's respective time that occured.

        Parameters
        ----------
        index : int, index of self.user_data

        Returns
        -------
        com_df : pd.DataFrame

        """

        
        # create empty arrays
        com_df = pd.DataFrame()
        
        for comtext,comtime in self.com_match.items():      # iterate over file comment columns
                
            # find index for specified source and match string
            idx = getattr(string_filters, self.user_data.at[index, 'Search Function'],
                          )(self.file_data[comtext], self.user_data.at[index, 'Search Value'])
            
            # append to dataframe
            com_df[comtext] = idx                           # com text logic for detection
            com_df[comtime] = self.file_data[comtime]       # com time
            
        return com_df
     

    def get_comments_with_time(self, index_df, index_time, index_com, category):
        """
        

        Parameters
        ----------
        index_df : TYPE
            DESCRIPTION.
        index_time : TYPE
            DESCRIPTION.
        index_com : TYPE
            DESCRIPTION.
        category : TYPE
            DESCRIPTION.

        Returns
        -------
        full_df : TYPE
            DESCRIPTION.

        """
        
        # create array for full
        full_df = pd.DataFrame(columns = list(index_df.columns) + [category])
        
        # add comments to main df
        for i,comment in enumerate(index_com):
            
            # get comment index
            com_idx = index_com[comment]
            
            # get categories were comment is present
            temp_df = index_df[com_idx].copy()
            temp_df.at[:,category] = comment
            
            ## get labchart read index ##
               
            # get user selection
            user_time = self.user_data.at[i, 'Time Selection (min)'].split(':')
            user_time = np.array([int(x) for x in user_time]) *60 # convert to seconds
            
            # add to comment time
            fs = np.array(index_df['sampling_rate'][com_idx], dtype = float)                    # convert sampling rate form string to float
            temp_df.at[:,'start_time'] = index_time[comment][com_idx] + (user_time[0] * fs)     # get start time
            temp_df.at[:,'stop_time'] = index_time[comment][com_idx] + (user_time[1] * fs)      # get stop time
            
            # append to full dataframe
            full_df = full_df.append(temp_df)
            
        return full_df
    
    def add_comments_to_index(self, index_df): # for one category
        """
        
        """
        
        
        # get category
        category =self.user_data['Category'].unique()[0]
         
        # create empty arrays
        index_com = pd.DataFrame()
        index_time =  pd.DataFrame()
        
        # per comment group
        for i in range(len(self.user_data)): # iterate over user comment groups
            
            # get logic from all File comments
            com_df = self.get_index_per_comment(i)
                        
            # combine File logic
            text = com_df[self.com_text_cols] 
            time = com_df[self.com_time_cols]
            com_label, com_time = GetComments.get_index_file_com(text, time, self.user_data.at[i, 'Search Value'])
            
            # pass to dataframe
            index_com[self.user_data.at[i, 'Assigned Group Name']] = com_label
            index_time[self.user_data.at[i, 'Assigned Group Name']] = com_time
               
         # check if at least one condition is present in each experiment pooled from one group    
        if index_com.any(axis=1).all() == False:
            raise Exception('Comments were not detected in all files.') 
        
        # add present comments along with their time
        index_df = self.get_comments_with_time(index_df, index_time, index_com, category)
        
        # reset index
        index_df = index_df.reset_index()
        
        # drop nans
        index_df = index_df.dropna(axis='columns')
        
        return index_df, index_df.columns[index_df.columns.get_loc('stop_time')+1:]
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        