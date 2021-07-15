
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

# show range slider value
@app.callback( 
    Output('slider_label', 'children'),
    [Input('channel_slider', 'value')],
)
def generate_channel_fields(slider_value):
    return str(slider_value)


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








