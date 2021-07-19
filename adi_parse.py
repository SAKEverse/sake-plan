# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 13:31:17 2021

@author: panton01
"""

### ------------------------ IMPORTS -------------------------------------- ###
import os
from beartype import beartype
import numpy as np
import pandas as pd
import adi
### ------------------------------------------------------------------------###

class AdiParse:
    """
    """
    
    
    @beartype
    def __init__(self, file_path:str):
        """

        Parameters
        ----------
        file_path : str

        Returns
        -------
        None.

        """
        
        # pass to object properties
        self.file_path = file_path
        
        # get file name
        self.file_name = os.path.basename(self.file_path)
        
        # default to largest block in file
        fread = self.read_labchart_file()           # read file
        
        block_len = np.zeros(fread.n_records)       # create empty array for storage
        for block in range(fread.n_records):
            
            # get block length
           block_len[block] = fread.channels[0].n_samples[block]
       
        self.block = np.argmax(block_len)           # find the block with larger length
        
        del fread                                   # clear memory
    
    
    def read_labchart_file(self):
        """
        Creates read object for labchart file and passes to self

        Returns
        -------
        adi_obj : Labchart read object

        """
        
        # return labchart read object
        return adi.read_file(self.file_path)
    
    
    def get_channel_names(self):
        """
        Returns labchart names in a dataframe format.

        Returns
        -------
        df : pd.DataFrame

        """
        
        # read labchart file
        adi_obj = self.read_labchart_file()

        # define dataframe columns
        cols = {'channel_id', 'channel_name'}

        # create empty dataframe
        df = pd.DataFrame(data = np.zeros((adi_obj.n_channels, len(cols))), columns = cols, dtype = 'string')
        
        # iterate over channels and get names
        for ch in range(adi_obj.n_channels):
            
            # append channel info to dictionary
            df.at[ch, 'channel_id'] = str(ch)
            df.at[ch, 'channel_name'] = adi_obj.channels[ch].name
        
        return df
    
    
    def get_all_file_properties(self):
        """
        Extracts file name, channel names, index , comment text and time.
        These information are added to a pandas DataFrame

        Returns
        -------
        df : pd.DataFrame

        """
        
        # read labchart file
        adi_obj = self.read_labchart_file()
        
        # get channel names
        df = self.get_channel_names()
        
        # add file name
        df['file_name'] = self.file_name
        
        # add comments for each channel
        properties = {'text' : 'comment_', 'tick_position' : 'comment_time_'}
        
        # iterate over properties
        for key, val in properties.items():
            
            temp_coms = [] # creaty empty list
            for ch in range(adi_obj.n_channels): # iterate over channels
                
                # convert comments to flattened list
                temp_coms.append([getattr(x, key) for x in adi_obj.channels[ch].records[self.block].comments])
            
            # convert list to dataframe
            df_comments = pd.DataFrame(temp_coms)
            
            # add columns to dataframe
            for i in range(df_comments.shape[1]): # iterate over max number of comments
                
                # pass to dataframe
                df[val + str(i)] = df_comments.iloc[:,i]
            
        return df
            
        
    
    def get_unique_conditions(self):
        """
        Get unique conditions from channel names.
        
        For example
        ----------
        ch1 = m_wt_cus
        ch2 = f_ko_cussage
        ch3 = m_ko_cus
        
        unique_groups = [[m, f], [wt, ko], [cus, cussage]]

        Raises
        ------
        FileNotFoundError
            DESCRIPTION.

        Returns
        -------
        df : Pd. DataFrame of separated groups per channel
        unique_groups : List of lists with unique groups

        """
        
        # get channel names
        df = self.get_channel_names()
        
        # create empty list to store length of each condition
        condition_list = []
        
        for i,name in enumerate(df.channel_name): # iterate over channels
            
            # get list of conditions
            condition_list.append(name.split('_'))
         
        try:
            # convert to pandas dataframe
            df = pd.DataFrame(condition_list)
        except Exception as err:
            raise FileNotFoundError(f'Unable to read conditions.\n{err}')
        
        # get unique groups for each condition
        unique_groups = [df[column].unique().tolist() for column in df]
        
        return df, unique_groups
            
          
    @beartype
    def filter_names(self, filters:str):
        """
        Filters channels names and returns index

        Parameters
        ----------
        filters : str

        Returns
        -------
        idx : List : List with indices of channels that contain filter

        """
        
        # get channel names
        df = self.get_channel_names()
        
        # get index of channels that contain filter
        idx = df.index[df.channel_name.str.contains(filters, case=False)].to_list()
        return idx
            
    # create unique sets of attributes from channel names to autopopulate the user drop down menus        


if __name__ == '__main__':
    
    # initiate object        
    adi_parse= AdiParse(r'C:\Users\panton01\Desktop\example_files\#1animal_sdsda_wt.adicht')
    
    df =  adi_parse.get_all_file_properties()
    
    # adi_obj = adi_read.read_labchart_file()
    
    # df, unique_groups = adi_parse.get_unique_conditions()

    # df.to_csv('sankey_data.csv')
    #
    # idx = adi_read.filter_names('fc')
      
            
            
            
            
            
            
            
            
            
            
            
            
            
            