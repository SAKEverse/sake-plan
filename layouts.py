import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import dash_daq as daq
import pandas as pd


# Always present
layout1 =  html.Div(id = 'layout_channel', children=[

    dcc.Store(id='user_df', storage_type = 'session'),

    # 0- alers
    html.Div(id = 'alert_div', children =[ # show warnings
        dbc.Alert(id = 'alert_message',color="warning", dismissable=True), #, duration = 5000
    ]),

    # 1- generate button + field div
    html.Div(id='generate_plus_field_div', children=[

        html.Div(id = 'export_div', children=[ # invisible (used for export)
            dcc.Download(id='download_dataframe_csv') ]),

        html.Div( id='generate_div', children=[
            html.Button('Generate', id='generate_button', n_clicks=0,   
            ),]),

        html.Div(id='data_path_main_div', children = [ 
            dcc.Input(id='data_path_input', type='text', placeholder='Path to data folder'),
        ]),

    ]),


    # 2 create user table
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
                        'width': '150', 'minWidth': '100', 'maxWidth': '175'}
            )
    ]),

    # 2- add row button
     html.Div( id='add_row_button_div', children=[
            html.Button('Add row', id='add_row_button', n_clicks=0,   
            ),]),

    # tree group diagram
     html.Div(id='tree_plot_div', children=[
     ]),

])


