import pandas as pd


# Create dropdown column elements
dropdown_cols = ['Source', 'Search Function']
drop_options =[{'channel_order', 'file_name', 'channel_name', 'comment_text'},
{'contains', 'startswith', 'endswith', 'order', 'exact_match'}] 

def dashtable(df):
    """
    Convert df to appropriate format

    PARAMETERS
    ----------
    df: pd.DataFrame,
    
    OUTPUT
    ----------
    dash_cols: list containg columns for dashtable
    df: dataframe for dashtable
    drop_dict: dict containg dropdown list for dashtable

    """

    dash_cols = [] # create dashtable column names
    for x in df.columns :
        temp_dict = {'name':x,'id':x}
        if x in dropdown_cols:   
            temp_dict.update({'presentation': 'dropdown'})
        # append to list    
        dash_cols.append(temp_dict)

    # get dropdown contents for each column
    drop_dict = {}
    for i in range(len(dropdown_cols)): # loop through dropdown columns
            drop_list = []
            for x in drop_options[i]: # loop through column elements
                drop_list.append({'label': x, 'value': x})
            drop_dict.update({dropdown_cols[i]:{'options': drop_list, 'clearable':False}}) # append to dict
    return dash_cols, df, drop_dict


if __name__ == '__main__':

    df = pd.read_csv('example_data/default_table_data.csv')
    dash_cols, df, drop_dict = dashtable(df)
    print(drop_dict)