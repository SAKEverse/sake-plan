# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 14:14:29 2021

@author: panton01
"""
import numpy as np
import pandas as pd

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
    
    # find index of channel order fields
    idx = user_data['Source'] == 'channel_order'
    
    # get data containing channel order
    channel_order = user_data[idx]
    
    # sort by order number
    channel_order = channel_order.sort_values(by=['Search Value'])
    
    # get order and channel names in 
    order = list(channel_order['Search Value'])
    regions = list(channel_order['Assigned Group Name'])
    
    # find integers
    integers = [s for s in order if s.isdigit()]
    
    if len(order) != len(integers):
        raise('Channel order option accepts only integers. e.g.: 1,2,3')
        
    if len(order) != len(regions):
        raise('Each group name requires an order number')
        
    if len(set(order)) != len(order):
        raise('Each number in channel order must be unique. Got:', order, 'instead')
        
    return regions


def contains(df_series, match:str):
    """
    Filter pd.series with string and get index

    Parameters
    ----------
    df_series : pd.Series
    match : str, to search the series
    
    Returns
    -------
    idx: bool

    """
    return np.array(df_series.str.contains(match))
    
def endswith(df_series, match:str):
    """
    Filter pd.series with string and get index

    Parameters
    ----------
    df_series : pd.Series
    match : str, to search the series
    
    Returns
    -------
    idx: bool

    """
    return np.array(df_series.str.endswith(match))
    
def startwith(df_series, match:str):
    """
    Filter pd.series with string and get index

    Parameters
    ----------
    df_series : pd.Series
    match : str, to search the series
    
    Returns
    -------
    idx: bool

    """
    return np.array(df_series.str.startwith(match), dtype = bool)