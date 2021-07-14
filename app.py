
### ---------------------------- Imports ---------------------------- ###
import os
import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
from dash.exceptions import PreventUpdate

### ------------- USER -------------- ###
from adi_read import AdiParse

### ----------------------------------------------------------------- ###


# init dash app with css style sheets
app = dash.Dash(__name__ , external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'] )

app.layout = html.Div(id = 'page-content', children=[

    # add data from path
    html.Div(id='data_path_main_div', 
        children = [ 
            html.Div(id='data_path_main_text', children = ['Data Path']),
            dcc.Input(id='data_path_input', type='text', placeholder='C:/'),
            html.Div(id='out_all_types'),
        ]),

    # Generate button
    html.Div( children =[
        html.Button('Generate', id='generate_button', n_clicks=0,
                style = {'color': 'white','background-color': '#4CAF50'}),
            ]),


# end of layout
])



### ------------------- Define callbacks ------------------- ###


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

        # export to csv
        df.to_csv('sankey_data.csv')

    except Exception as err:
        return 'Got ' + str(folder_path) + ': ' + str(err)
    return str(folder_path)



if __name__ == '__main__':

    app.run_server(debug = True,
                    port = 80,
                    # host = '127.0.0.1',
                   )








