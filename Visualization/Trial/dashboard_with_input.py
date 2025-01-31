import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
# matplot

import pandas as pd
import numpy as np
import plotly.express as px

from Visualization.Trial import dash_upload_and_result

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = dash_upload_and_result.upload_div()


@app.callback(Output('intermediate-value', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        df = dash_upload_and_result.parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])

        df[['HomeGoals', 'AwayGoals']] = df.Result.str.split('-', expand=True, )
        df['HomeGoals'] = pd.to_numeric(df['HomeGoals'], errors='coerce').fillna(0).astype(int)
        df['AwayGoals'] = pd.to_numeric(df['AwayGoals'], errors='coerce').fillna(0).astype(int)
        df['HomeDiff'] = df.HomeGoals - df.AwayGoals
        df['AwayDiff'] = df.AwayGoals - df.HomeGoals

        json_obj = df.to_json(date_format='iso', orient='split')
        return json_obj
        # return dash_table.DataTable(
        #      data=df.to_dict('records'),
        #      columns=[{'name': i, 'id': i} for i in df.columns]
        # )
        # df.to_json(date_format='iso', orient='split')
        # return dash_table.DataTable(
        #     data=df.to_dict('records'),
        #     columns=[{'name': i, 'id': i} for i in df.columns]
        # ),


@app.callback(Output('output-data-upload', 'children'),
              Input('intermediate-value', 'data'))
def update_output(jsonified_data):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        )


@app.callback(Output('output-data-bar-chart', 'figure'),
              Input('intermediate-value', 'data'))
def visualize_output(jsonified_data):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        grouped_home = df.groupby('Home Team', as_index=False).agg({"HomeDiff": "sum"})
        grouped_away = df.groupby('Away Team', as_index=False).agg({"AwayDiff": "sum"})

        grouped_home.columns = ['Team', 'GoalDiff']
        grouped_away.columns = ['Team', 'GoalDiff']

        grouped_contact = pd.concat([grouped_home, grouped_away])
        grouped_all = grouped_contact.groupby('Team', as_index=False).agg({"GoalDiff": "sum"})

        labels = ['Team']
        values = grouped_all

        grouped_all["Color"] = np.where(grouped_all["GoalDiff"] < 0, 'red', 'green')

        chart = px.bar(grouped_all, x="GoalDiff", y="Team", color="Color", color_discrete_sequence=["red", "green"])

        return chart
    else:
        return px.bar()
        # chart = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

        #return chart


# @app.callback(Output('output-data-pie-chart', 'children'),
#               Input('upload-data', 'contents'),
#               State('upload-data', 'filename'),
#               State('upload-data', 'last_modified'))
# def visualize_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         df = DashUpload.parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
#
#         df[['HomeGoals', 'AwayGoals']] = df.Result.str.split('-', expand=True, )
#         df['HomeGoals'] = pd.to_numeric(df['HomeGoals'], errors='coerce').fillna(0).astype(int)
#         df['AwayGoals'] = pd.to_numeric(df['AwayGoals'], errors='coerce').fillna(0).astype(int)
#         df['HomeDiff'] = df.HomeGoals - df.AwayGoals
#         df['AwayDiff'] = df.AwayGoals - df.HomeGoals
#
#         groupedHome = df.groupby('Home Team', as_index=False).agg({"HomeDiff": "sum"})
#         groupedAway = df.groupby('Away Team', as_index=False).agg({"AwayDiff": "sum"})
#
#         groupedHome.columns = ['Team', 'GoalDiff']
#         groupedAway.columns = ['Team', 'GoalDiff']
#
#         groupedConcat = pd.concat([groupedHome, groupedAway])
#         groupedAll = groupedConcat.groupby('Team', as_index=False).agg({"GoalDiff": "sum"})
#
#         labels = ['Team']
#         values = groupedAll
#
#         chart = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
#         return chart


if __name__ == '__main__':
    app.run_server(debug=True)
