import pandas as pd
from adi_parse import AdiParse


# get user table data example
user_data = pd.read_csv('example_data/default_table_data.csv')

# 1 Get channel order if exists

idx = user_data['Source'] == 'channel_order'

channel_order = user_data[idx]
channel_order = channel_order.sort_values(by=['Search Value'])
order = list(user_data['Search Value'][idx])
regions = list(user_data['Assigned Group Name'][idx])

integers = [s for s in order if s.isdigit()]

if len(order) != len(integers):
    raise('Channel order option accepts only integers. e.g.: 1,2,3')
    
if len(order) != len(regions):
    raise('Each group name requires an order number')
    
if len(set(order)) != len(order):
    raise('Each number in channel order must be unique. Got:', order, 'instead')

# if __name__ == '__main__':
    
#     file_path = r'C:\Users\panton01\Desktop\example_files\#1animal_sdsda_wt.adicht'
#     channel_order = ['Bla', 'Hipp', 'Emg']
#     # initiate object      
#     adi_parse= AdiParse(file_path, channel_order)