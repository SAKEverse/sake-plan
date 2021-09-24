
### ---------------------------- Imports ---------------------------- ###
import os, shutil, json
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import session


# User Defined #
from app import app
from layouts import layout1
import dash_bootstrap_components as dbc
from adi_parse import AdiParse
from create_user_table import dashtable
from tree import drawSankey
from filter_table import get_index_array
# import callbacks
### ----------------------------------------------------------------- ###


# init dash app with css style sheets
# apply general css styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets) #, external_stylesheets=[, dbc.themes.BOOTSTRAP]
app.server.secret_key = os.urandom(24)

# Define main layout
app.layout = html.Div(children = [
    
    html.Div(children = layout1), 
])

# update dataframe
@app.callback(
    Output('user_df', 'data'),
    [Input('user_table', 'data'),]
   
    )
def get_data_at_start(table_data):
    
    # convert data to dataframe
    df = pd.DataFrame(table_data)
 
    return df.to_json(date_format='iso', orient='split')



### ---------- Update Colony Table--------- ###
@app.callback(
    [Output('user_table', "columns"), 
    Output('user_table', 'data'),
    Output('user_table', 'row_deletable'),
    Output('user_table', 'dropdown')
    ],
    [Input("add_row_button","n_clicks"),
    State('user_df', 'data')],
    
    )
def update_usertable(n_clicks, json_data):

    # if dataframe doesn't read default from memory
    if json_data == None:
        # get default dataframe
        df = pd.read_csv(user_table_path)
    else:
        # get data from user datatable
        df = pd.read_json(json_data, orient='split')

    # conver user data in dashtable format
    dash_cols, df, drop_dict = dashtable(df) 

    if n_clicks > 0: # Add rows when button is clicked
        
        a = np.empty([1, len(df.columns)],dtype=object) # create empty numpy array
        a[:] = '' # convert all to nans
        a[0][-1]='all'
        append_df = pd.DataFrame(a, columns = df.columns) # create dataframe
        df = df.append(append_df, ignore_index=True) # append dataframe

    return dash_cols, df.to_dict('records'), True, drop_dict


# Retrieve path and plot tree diagram
@app.callback(
    [Output('alert_div', 'children'),
     Output('tree_plot_div', 'children'),
     Output('download_dataframe_csv', 'data'),
     Output('download_user_data_csv', 'data')],
    [Input('generate_button', 'n_clicks')],
    [State('data_path_input', 'value'),
    State('user_table', 'data')],
)
def update_output(n_clicks, folder_path, user_data):

    try:
        if folder_path is None:         
            warning = None
            fig = None
            data = None
            user_data_export = None
        else:

            # get grouped dataframe
            index_df, group_names, warning_str = get_index_array(folder_path, user_data)

            # Get tree plot as dcc graph
            fig = dcc.Graph(id = 'tree_structure', figure = drawSankey(index_df[group_names]))

            # send index_df for download
            data = dcc.send_data_frame(index_df.to_csv, 'index.csv', index = False)

            # send user data for download
            user_data = pd.DataFrame(user_data)
            user_data_export = dcc.send_data_frame(user_data.to_csv, 'user_data.csv', index = False)

            warning = dbc.Alert(id = 'alert_message', children = [str(warning_str)], color="warning", dismissable=True)
        return warning, fig, data, user_data_export

    except Exception as err:
        warning = dbc.Alert(id = 'alert_message', children = ['   ' + str(err)], color="warning", dismissable=True) #, duration = 10000
        return warning, None, None, None


if __name__ == '__main__':

    user_table_path = 'example_data/default_table_data.csv'

    app.run_server(debug = True,
                    port = 8050,
                    host = 'localhost',
                   )








