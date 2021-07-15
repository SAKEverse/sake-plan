
### ---------------------------- Imports ---------------------------- ###
import os
import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


# User Defined #
from app import app
from layouts import layout_common, layout_channel, layout_file
from adi_read import AdiParse
# import callbacks
### ----------------------------------------------------------------- ###


# init dash app with css style sheets
app = dash.Dash(__name__ , external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'] )


# Define main layout
app.layout = html.Div(children = [
    
    html.Div(children = layout_common),
    
    # Callback layout
    html.Div(id='selected_layout'),
])

def create_channel_divs(ch_num):
    return html.Div(
                dcc.Input(
                id='input_{}'.format(ch_num),
                type='text',
                placeholder='Channel {}'.format(ch_num),
                ), style={'padding': '0px 10px'})


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
    divs=[] # create list with divs
    for ch_num in range(channel_numbers):
        divs.append(create_channel_divs(ch_num))
    return divs

# Generate fields for unique channels
@app.callback( 
    Output('channel_inputs', 'children'),
    [Input('input_1', 'value'),
    Input('input_2', 'value')],
)
def get_channels(ch_input):
    return ch_input

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








