
### ---------------------------- Imports ---------------------------- ###
import dash, dash_table
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
### ----------------------------------------------------------------- ###


# init dash app with css style sheets
app = dash.Dash(__name__ , external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'] )

app.layout = html.Div(id = 'page-content', children=[


])



if __name__ == '__main__':

    app.run_server(debug = True,
                    port = 80,
                    # host = '127.0.0.1',
                   )








