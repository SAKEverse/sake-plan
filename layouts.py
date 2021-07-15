import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

# Always present
layout_common =  html.Div(id = 'layout_channel', children=[

    #1- Separation type dropdown
    html.Div( id='main_dropdown_div', children = [
        dcc.Dropdown(
            id='main_dropdown', className='dcc_dropdown',
            options=[
                {'label': 'Separate by channel names', 'value': 'channel_name'},
                {'label': 'Separate by file name', 'value':  'file_name'},
            ], value='channel_name', clearable=False),
    ]),

    # 2- Input data path
    html.Div(id='data_path_main_div', 
        children = [ 
            # html.Div(id='data_path_main_text', children = ['Data Path']),
            dcc.Input(id='data_path_input', type='text', placeholder='Path-to-data'),
            html.Div(id='out_all_types'),
    ]),

    # 3- Generate plot and table button
    html.Div( id='generate_div', children =[
        html.Button('Generate', id='generate_button', n_clicks=0,   
        ),
    ]),

]) # end of this layout


# If files are grouped by channel name
layout_file =  html.Div(id = 'layout_file_name', children=[

    # 1- Unique Channels
    html.Div(id='unique_channels_div', 
        children = [ 

        # unique channel number     
        daq.NumericInput(
            id='unique_channel_number',
            value=3
        ),
        html.Div(id = 'unique_channel_label_container', children =[
        html.Div(id= 'unique_channel_label', children = 'Unique Channels'),
        ]),
        ]),

    # 3- Unique channel field
    html.Div(id='unique_channels_inputs'),


    # 4- Unique channel field
    html.Div(id='channel_inputs'),

]) # end of this layout


# If files are grouped by file name
layout_channel =  html.Div(id = 'layout_file_name', children=[

    # 1- Example
    html.Div(id='tree_plot_div'
        ),
   
]) # end of this layout