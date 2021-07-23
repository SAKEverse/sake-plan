# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 10:59:45 2021

@author: panton01
"""

from beartype import beartype
import numpy as np
import pandas as pd
import string_filters



def get_index_file_com(com_logic_df, time_array, label):
        """
        
    
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


class GetComments:
    
    
    def __init__(self, file_data, user_data, comment_text, comment_time, fs = 4000):

        
        # pass to object
        self.comment_text = comment_text
        self.comment_time = comment_time

        # Get matching comment text and time columns from file_data dataframe
        self.com_text_cols = list(file_data.columns[file_data.columns.str.contains(self.comment_text)])
        self.com_time_cols = list(file_data.columns[file_data.columns.str.contains(self.comment_time)])
        self.com_match = dict(zip(self.com_text_cols, self.com_time_cols))
        
        # pass file data to object
        self.file_data = file_data
        self.fs = fs
        
        # get user data containing comment text
        self.user_data = user_data[user_data['Source'] == self.comment_text].reset_index()
        
        # get groups
        self.com_categories = list(self.user_data.Category.unique())
       
    
    def get_index_per_comment(self, index):

        
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



    
    def add_coms_to_index(df):
        print('test')
        
        
    
    
    def add_comments_to_index(self):
        
        
        # create empty arrays
        index_df = pd.DataFrame()
            
        for i in range(len(self.user_data)): # iterate over user comment groups
            
            # get logic from all File comments
            com_df = self.get_index_per_comment(i)
                        
            # combine File logic
            text = com_df[self.com_text_cols]; time = com_df[self.com_time_cols]
            com_label, com_time = get_index_file_com(text, time, self.user_data.at[i, 'Search Value'])
            
            # pass to dataframe
            index_df[self.user_data.at[i, 'Assigned Group Name']] = com_label
        
        
        print('test')
    
    
    
    
    
    
            # get comment times
        # user_time = user_com_text.at[i, 'Time Selection (min)'].split(':')
        # user_time = np.array([int(x) for x in user_time])* fs*60
        
        # # get comment index
        # com_idx = np.argmax(np.array(com_text_df), axis = 1)
        # idx = np.zeros((com_idx.shape[0],2))
        
        # for ii in range(len(com_text_df)):
            
        #     # get index of where comment was detected
        #     idx_one = np.where(com_text_df.iloc[ii,:] == True)[0]
                           
        #     if len(idx_one) == 0: # if no comment was detected
        #         idx[ii] = file_data['file_length'][ii]
        #     else:
        #         idx[ii,:] = int(float(com_time_array[ii,idx_one[0]])) + user_time
                           
        # add comment to index
        # index.update({user_data.at[i, 'Assigned Group Name']: idx})
        
    
    # for i in len(com_text_df):
        
        # com_text_df.at[i,'time'] = com_time_array[np.array(com_text_df)]
    
    # #



        