import base64
import datetime
import io
import matplotlib
matplotlib.use('Agg')
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table, callback_context
import numpy as np
import pandas as pd
import pandas_profiling as pp
from pandas_profiling import ProfileReport


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Button('Pandas Profiling Report', id='submit-val'),
    html.Div(id='output-data-upload'),
    
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
           
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
          
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


def profiling (df):
        
      
        profile = ProfileReport(df, title="Pandas Profiling Report")
       
        profile.to_file("./assets/rapport.html")


@app.callback(Output('output-data-upload', 'children'),

              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              Input('submit-val', 'n_clicks'))


def update_output(list_of_contents, list_of_names, list_of_dates,bn):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        changed_id = [p['prop_id']for p in callback_context.triggered][0]    
        if 'submit-val' in changed_id:
            profiling(children[0])

            return html.Iframe(src= "assets/rapport.html",  style={"height": "1067px", "width": "100%"})
        return "children"
    return ""    

       

if __name__ == '__main__':
    app.run_server(debug=True)
