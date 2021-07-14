# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 13:31:17 2021

@author: panton01
"""

### ------------------------ IMPORTS -------------------------------------- ###
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
    adi_read = AdiParse(r'Z:\Pantelis\example_ch_names.adicht')
    
    df, unique_groups = adi_read.get_unique_conditions()

    df.to_csv('sankey_data.csv')
    #
    # idx = adi_read.filter_names('fc')
      
            
            
            
            
            
            
            
            
            
            
            
            
            
            