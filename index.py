
### ---------------------------- Imports ---------------------------- ###
import os, shutil, json
import numpy as np
import pandas as pd
import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import session


# User Defined #
from app import app
from layouts import layout1
from adi_parse import AdiParse
from create_user_table import dashtable
from tree import drawSankey
from filter_table import get_index_array
# import callbacks
### ----------------------------------------------------------------- ###


# init dash app with css style sheets
app = dash.Dash(__name__ , external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'] )
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
def colony_update(n_clicks, json_data):

    # if dataframe doesn't read default from memory
    if json_data == None:
        # get default dataframe
        df = pd.read_csv(user_table_path)
    else:
        # get data in dash table format
        df = pd.read_json(json_data, orient='split')

    # get data in dashtable format
    dash_cols, df, drop_dict = dashtable(df) 

    if n_clicks > 0: # Add rows when button is clicked
        
        a = np.empty([1, len(df.columns)]) # create empty numpy array
        a[:] = np.nan # convert all to nans
        append_df = pd.DataFrame(a, columns = df.columns) # create dataframe
        df = df.append(append_df, ignore_index=True) # append dataframe

    return dash_cols, df.to_dict('records'), True, drop_dict


# Retrieve path and plot tree diagram
@app.callback(
    [Output('out_all_types', 'children'),
     Output('tree_plot_div', 'children'),
     Output('download_dataframe_csv', 'data')],
    [Input('generate_button', 'n_clicks')],
    [State('data_path_input', 'value'),
    State('user_table', 'data')],
)
def update_output(n_clicks, folder_path, user_data):

    if folder_path is None:
        folder_path = 'empty'
    try:

        # get grouped dataframe
        df, group_names = get_index_array(folder_path, user_data);

        # Get tree plot as dcc graph
        graph = dcc.Graph(id = 'tree_structure', figure =  drawSankey(df[group_names]))

    except Exception as err:
        return 'Got ' + str(folder_path) + ': ' + str(err)
        
    return str(folder_path), graph, dcc.send_data_frame(df.to_csv, 'index.csv')


if __name__ == '__main__':

    user_table_path = 'example_data/default_table_data.csv'

    app.run_server(debug = True,
                    port = 8050,
                    host = 'localhost',
                   )








