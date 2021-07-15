
### ---------------------------- Imports ---------------------------- ###
import os
import pandas as pd
import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import session


# User Defined #
from app import app
from layouts import layout_common, layout_channel, layout_file
from adi_read import AdiParse
# import callbacks
### ----------------------------------------------------------------- ###


# init dash app with css style sheets
app = dash.Dash(__name__ , external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'] )
app.server.secret_key = os.urandom(24)

# Define main layout
app.layout = html.Div(children = [
    
    html.Div(children = layout_common),
    
    # Callback layout
    html.Div(id='selected_layout'),
])


def create_channel_table(input_list):
    # create dataframe
    df = pd.DataFrame(data = [str(x) for x in input_list], 
    columns ={'channel_id'})

    # get columns in right format
    cols = [] # create dashtable column names
    for x in df.columns :
        temp_dict = {'name':x,'id':x}
        # append to list    
        cols.append(temp_dict)

    # create datatable
    table = dash_table.DataTable(id = 'channel_table',
                editable = True,
                columns = cols,
                data = df.to_dict('records'),
                style_cell={
                        'color': 'black',
                        'textAlign': 'center',
                        'font-family':'arial',
                        'font-size': '100%',
                        },
                    style_header={
                        'fontWeight': 'bold',
                        'color': 'black',
                        'textAlign': 'center',
                        'backgroundColor': 'rgb(230, 230, 230)',
                    },
                )
    return table

# get layout depending on grouping selection
@app.callback( 
    Output('selected_layout', 'children'),
    [Input('main_dropdown', 'value')],
)
def get_layout(dropdown_value):
    if dropdown_value == 'channel_name':
        return layout_channel
    elif dropdown_value == 'file_name':
        return layout_file


# Generate fields for unique channels
@app.callback( 
    Output('unique_channels_inputs', 'children'),
    [Input('unique_channel_number', 'value')],
)
def generate_channel_fields(channel_numbers):

    # get table entries
    session.update({'unique_channels':['channel_' + str(x) for x in range(channel_numbers)]})
          
    return create_channel_table(session['unique_channels'])

# Get data from table
@app.callback( 
    Output('channel_inputs', 'children'),
    [Input('channel_table', 'data')],
)
def get_channels(data):
    session.update({'unique_channels':[x['channel_id'] for x in data]})

    # return create_channel_table(session['unique_channels'])

# Retrieve path and plot tree diagram
@app.callback(
    Output('out_all_types', 'children'),
    [Input('generate_button', 'n_clicks')],
    [State('data_path_input', 'value')],
)
def update_output(n_clicks, folder_path):

    if folder_path is None:
        folder_path = 'empty'
    try:
        # initiate object        
        adi_read = AdiParse(folder_path)

        # get grouped dataframe
        df, unique_groups = adi_read.get_unique_conditions()

        # Get sankey plot
        # df.to_csv('sankey_data.csv')

    except Exception as err:
        return 'Got ' + str(folder_path) + ': ' + str(err)
    return str(folder_path)


if __name__ == '__main__':

    app.run_server(debug = True,
                    port = 8050,
                    host = 'localhost',
                   )








