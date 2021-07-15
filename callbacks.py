from app import app
from dash.dependencies import Input, Output, State
# ------------- USER -------------- #
from adi_read import AdiParse
# --------------------------------- #



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
