
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import io
import pandas as pd

import dash_table
import base64
import dash_html_components as html

from app import app

#TODO fix parse_contents method & callbacks for uploading data
@app.callback(
    Output('editing-table-data-output', 'children'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename')]
)
def update_table(contents, filename):
    #TODO move 'layout' contents to home.py 
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_contents(contents, filename)

        table = html.Div(
            [
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict("rows"),
                    columns=[{"name": i, "id": i} for i in df.columns],
                ),
            ]
        )

    return table

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    if 'xls' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded), sheet_name='cpctws')
        #TODO make separate dataframes for each sheet or do that in update_table method?
    else:
        pass
    print(df)
    return df