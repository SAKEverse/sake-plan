import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
import pandas as pd


# Always present
layout1 =  html.Div(id = 'layout_channel', children=[

    html.Div(id = 'hidden_div', children=[], hidden=True),
    dcc.Store(id='user_df'),

    # 1- generate button + field div
    html.Div(id='generate_plus_field_div', children=[

        html.Div( id='generate_div', children=[
            html.Button('Generate', id='generate_button', n_clicks=0,   
            ),]),

        html.Div(id='data_path_main_div', 
            children = [ 
                dcc.Input(id='data_path_input', type='text', placeholder='Path-to-data'),
                html.Div(id='out_all_types'),
        ]),
    ]),

    # 2- User table
     html.Div( id='add_row_button_div', children=[
            html.Button('Add row', id='add_row_button', n_clicks=0,   
            ),]),

    # create datatable
    html.Div(id='user_table_div', children=[

        dash_table.DataTable(id = 'user_table',
                    editable = True,
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
                    style_data={
                        'width': '125px', 'minWidth': '125px', 'maxWidth': '125px'}
            )
    ]),

])


