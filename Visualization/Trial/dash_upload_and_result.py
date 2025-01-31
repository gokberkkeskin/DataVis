import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html

from dash import dash_table
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


def upload_div():
    pie_chart_image = base64.b64encode(open('../images/pie_chart.png', 'rb').read())
    stadium_image = base64.b64encode(open('../images/stadium.png', 'rb').read())
    return html.Div(children=[
        html.Div([
            #html.H1(children='G-Dash'),
            #html.Div(html.Img(src='images/pie_chart.png')),
            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(pie_chart_image.decode()), width=45),
                html.H2(children='G-Dash')
                ]),

            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(stadium_image.decode()), width=45),
                html.H3(children='Football Stats Analyzer')
            ]),

            html.Button(children='test') ,
            # dcc.Markdown('''
            #     ## G-Dash
            #
            #     ---
            #     ### _Football Stats Analyzer_
            #
            #     ---
            # '''),
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
                # (try single file later. Now it fails because in callback i try to process a list not one element)
                multiple=True
            )
        ]),

        dcc.Graph(id='output-data-bar-chart'),
        html.Div(id='output-data-upload'),
        dcc.Store(id='intermediate-value')
    ])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), sep=';')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


