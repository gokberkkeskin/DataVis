"""
This app creates a dashboard webpage with a sidebar on the left
"""
import base64

import dash
import dash_bootstrap_components as dbc
# import dash_html_components
import sqlparse
from dash import html
import numpy as np
import pandas as pd
from dash import Input, Output, dcc, html, State, dash_table
import plotly.express as px
from sql_metadata import Parser, QueryType

from Visualization import dash_upload
from Visualization import database_oper
import sqlite3 as sl

THEME = dbc.themes.MATERIA
app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

pie_chart_image = base64.b64encode(open('images/pie_chart.png', 'rb').read())
stadium_image = base64.b64encode(open('images/stadium.png', 'rb').read())


merge_button = [
    dbc.Button(
        "Merge",
        id="button-merge",
        color="primary",
        disabled=True,
        n_clicks=0
    )
]

sidebar = html.Div(
    [
        dbc.Row([
            dbc.Col(html.Img(src='data:image/png;base64,{}'.format(pie_chart_image.decode()), width=45), width=3),
            dbc.Col(html.H4("DataVis", className="display-6"))
        ]
        ),
        html.Hr(),
        html.P(
            "Online analytics", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Goal Differences", href="/goal-diff", active="exact"),
                dbc.NavLink("Quick Comparison", href="/quick-comparison", active="exact"),
                dbc.NavLink("Quick Comparison DB", href="/quick-comparison-db", active="exact"),
                dbc.NavLink("About", href="/about", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

df_dbs = database_oper.list_databases()

div_id_dd_1 = html.Div([
    dcc.Dropdown(
        id='dd-dropdown-1',
        options=[
            {'label': lbl, 'value': val} for lbl, val in zip(df_dbs['DB_NAME'], df_dbs['DB_PATH'])
        ]
    )
])


div_id_dd_2 = html.Div([
    dcc.Dropdown(
        id='dd-dropdown-2',
        options=[
            {'label': lbl, 'value': val} for lbl, val in zip(df_dbs['DB_NAME'], df_dbs['DB_PATH'])
        ]
    )
])


comparison_content = html.Div(
    [
        dbc.Row([
            dbc.Col(html.P("File selection 1")),
            dbc.Col(html.P("File selection 2"))
        ]
        ),
        dbc.Row([
            dbc.Col(dash_upload.upload_div('intermediate-value-file-comparison-1', 'upload-data-file-comparison-1')),
            dbc.Col(dash_upload.upload_div('intermediate-value-file-comparison-2', 'upload-data-file-comparison-2'))
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='output-processed-filename-file-comparison-1')),
            dbc.Col(html.Div(id='output-processed-filename-file-comparison-2'))
        ]),
        html.Hr(),
        html.P("Comparison Criteria"),
        html.Hr(),
        dbc.Row([
            dbc.Col(html.Div(id='output-processed-filename-file-comparison-1')),
            dbc.Col(html.Div(id='output-processed-filename-file-comparison-2'))
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='output-columns-file-1')),
            dbc.Col(html.Div(id='output-columns-file-2'))
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='output-file-preview-comparison-1')),
            dbc.Col(html.Div(id='output-file-preview-comparison-2'))
        ]),
        html.Hr(),
        html.Div(merge_button),
        dcc.Store(id='intermediate-value-comparison-result'),
        dbc.Row([
            dbc.Col(html.Div(id='comparison-result'))
        ]),

        html.Hr(),
        html.P("Results"),
        html.Hr(),

        dbc.Row([
            dbc.Col(html.Div(id='comparison-result2'))
        ])

    ],
    # style=CONTENT_STYLE,
)

comparison_content_db = html.Div(
    [
        dbc.Row([
            dbc.Col(html.P("DB selection 1")),
            dbc.Col(html.P("DB selection 2"))
        ]
        ),
        dbc.Row([
            dbc.Col(div_id_dd_1),
            dbc.Col(div_id_dd_2),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(html.Div(id='dd-output-table-1')),
            dbc.Col(html.Div(id='dd-output-table-2'))
        ]),
        html.Br(),
        # html.Hr(),
        # html.P("Query"),
        # html.Hr(),
        dbc.Row([
            dbc.Col(html.Div(id='input-query')),
        ]),
        # html.Hr(),
        # html.P("Results"),
        # html.Hr(),
        dbc.Row([
            dbc.Col(html.Div(id='output-query'))
        ]),
    ],
    # style=CONTENT_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("Welcome to your tailored fit online analytics site!")

    elif pathname == "/goal-diff":
        file_uploader_football = dash_upload.upload_div('intermediate-value-football', 'upload-data-football')
        uploaded_file_panel_football = html.Div(id='output-processed-filename-football')
        bar_chart = dcc.Graph(id='output-data-bar-chart-football')
        data_table_football = html.Div(id='output-data-upload-football')
        return html.Div([file_uploader_football, uploaded_file_panel_football, bar_chart, data_table_football])

    elif pathname == "/quick-comparison":
        return html.Div([comparison_content])

    elif pathname == "/quick-comparison-db":
        return html.Div([comparison_content_db])

    elif pathname == "/about":
        return html.P("About...")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"Requested url {pathname} can not be found..."),
        ]
    )


def show_filename_component(filename):
    if filename is not None:
        return html.Div(
            [
                html.P(
                    [
                        "Uploaded Filename ",
                        html.Span(
                            filename,
                            id="tooltip-target"+str(filename),
                            style={"textDecoration": "underline", "cursor": "pointer"},
                        ),
                    ]
                ),
                dbc.Tooltip(
                    "Full path of the file not shown due to security reasons",
                    target="tooltip-target"+str(filename),
                )
            ]
        )
    else:
        return None


def show_preview_component(jsonified_data, filename):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        dt = dash_table.DataTable(
            data=df.head().to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
        )
        return html.Div(
            [
                html.Span(
                    "Preview",
                    id="hover-target"+str(filename),
                    style={"textDecoration": "underline", "cursor": "pointer"},
                ),
                dbc.Popover(
                    dt,
                    target="hover-target"+str(filename),
                    trigger="hover",
                    placement="bottom"
                )
            ]
        )
    else:
        return None


# ---------------------------------------------------------------
# Football functions


@app.callback(Output('intermediate-value-football', 'data'),
              Input('upload-data-football', 'contents'),
              State('upload-data-football', 'filename'),
              State('upload-data-football', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        df = dash_upload.parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])

        df[['HomeGoals', 'AwayGoals']] = df.Result.str.split('-', expand=True, )
        df['HomeGoals'] = pd.to_numeric(df['HomeGoals'], errors='coerce').fillna(0).astype(int)
        df['AwayGoals'] = pd.to_numeric(df['AwayGoals'], errors='coerce').fillna(0).astype(int)
        df['HomeDiff'] = df.HomeGoals - df.AwayGoals
        df['AwayDiff'] = df.AwayGoals - df.HomeGoals

        json_obj = df.to_json(date_format='iso', orient='split')
        return json_obj


@app.callback(Output('output-processed-filename-football', 'children'),
              Input('upload-data-football', 'filename'))
def show_filename(filename):
    return show_filename_component(filename)


@app.callback(Output('output-data-upload-football', 'children'),
              Input('intermediate-value-football', 'data'))
def update_output(jsonified_data):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        return html.Div([
            # dbc.Table.from_dataframe(
            #     df,
            #     striped=True,
            #     bordered=True,
            #     hover=True,
            #     index=True,
            #     filter_action="native",
            #     sort_action="native"
            # )
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                style_cell={'fontSize': 14, 'font-family': 'sans-serif'},
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_deletable=False,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=15,
            )
        ])


@app.callback(Output('output-data-bar-chart-football', 'figure'),
              Input('intermediate-value-football', 'data'))
def visualize_output(jsonified_data):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        grouped_home = df.groupby('Home Team', as_index=False).agg({"HomeDiff": "sum"})
        grouped_away = df.groupby('Away Team', as_index=False).agg({"AwayDiff": "sum"})

        grouped_home.columns = ['Team', 'GoalDiff']
        grouped_away.columns = ['Team', 'GoalDiff']

        grouped_contact = pd.concat([grouped_home, grouped_away])
        grouped_all = grouped_contact.groupby('Team', as_index=False).agg({"GoalDiff": "sum"})

        grouped_all["Color"] = np.where(grouped_all["GoalDiff"] < 0, 'red', 'green')
        chart = px.bar(grouped_all, x="GoalDiff", y="Team", color="Color", color_discrete_sequence=["red", "green"])

        return chart
    else:
        return {
            "layout": {
                "xaxis": {
                    "visible": "false"
                },
                "yaxis": {
                    "visible": "false"
                },
                "annotations": [
                    {
                        "text": "Upload soccer scores file to see results",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": "false",
                        "font": {
                            "size": 14
                        }
                    }
                ]
            }
        }

# ---------------------------------------------------------------
# Comparison Functions


@app.callback(Output('intermediate-value-file-comparison-1', 'data'),
              Input('upload-data-file-comparison-1', 'contents'),
              State('upload-data-file-comparison-1', 'filename'),
              State('upload-data-file-comparison-1', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        df_file1 = dash_upload.parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        json_obj = df_file1.to_json(date_format='iso', orient='split')
        return json_obj


@app.callback(Output('output-processed-filename-file-comparison-1', 'children'),
              Input('upload-data-file-comparison-1', 'filename'))
def show_filename(filename):
    return show_filename_component(filename)


@app.callback(Output('intermediate-value-file-comparison-2', 'data'),
              Input('upload-data-file-comparison-2', 'contents'),
              State('upload-data-file-comparison-2', 'filename'),
              State('upload-data-file-comparison-2', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        df_file2 = dash_upload.parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        json_obj = df_file2.to_json(date_format='iso', orient='split')
        return json_obj


@app.callback(Output('output-processed-filename-file-comparison-2', 'children'),
              Input('upload-data-file-comparison-2', 'filename'))
def show_filename(filename):
    return show_filename_component(filename)


@app.callback(Output('output-columns-file-1', 'children'),
              Input('intermediate-value-file-comparison-1', 'data'))
def show_columns(jsonified_data):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        radio_items = dcc.RadioItems(
            id='radio-items-1',
            options=[{'label': i, 'value': i} for i in df.columns],
            labelStyle={'display': 'block'}
        )
        return radio_items


@app.callback(Output('output-columns-file-2', 'children'),
              Input('intermediate-value-file-comparison-2', 'data'))
def show_columns(jsonified_data):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        radio_items = dcc.RadioItems(
            id='radio-items-2',
            options=[{'label': i, 'value': i} for i in df.columns],
            labelStyle={'display': 'block'}
        )
        return radio_items


@app.callback(Output('output-file-preview-comparison-1', 'children'),
              Input('intermediate-value-file-comparison-1', 'data'),
              Input('upload-data-file-comparison-1', 'filename'))
def show_preview(jsonified_data, filename):
    return show_preview_component(jsonified_data, filename)


@app.callback(Output('output-file-preview-comparison-2', 'children'),
              Input('intermediate-value-file-comparison-2', 'data'),
              Input('upload-data-file-comparison-2', 'filename'))
def show_preview(jsonified_data, filename):
    return show_preview_component(jsonified_data, filename)


@app.callback(Output('button-merge', 'disabled'),
              Input('upload-data-file-comparison-1', 'filename'),
              Input('upload-data-file-comparison-2', 'filename'),
              Input('radio-items-1', 'value'),
              Input('radio-items-2', 'value')
              )
def set_button_enabled_state(filename_1, filename_2, radio_item_1, radio_item_2):
    if filename_1 is None and filename_2 is None:
        return True
    elif radio_item_1 is None or radio_item_2 is None:
        return True
    else:
        return False


@app.callback(Output('intermediate-value-comparison-result', 'data'),
              Input('button-merge', 'n_clicks'),
              Input('intermediate-value-file-comparison-1', 'data'),
              Input('intermediate-value-file-comparison-2', 'data'),
              Input('radio-items-1', 'value'),
              Input('radio-items-2', 'value'),
              # Input('dt-compare', 'selected_columns')
              )
def on_button_click(n, file_1_data, file_2_data, radio_item_1, radio_item_2):
    if n is None or n == 0:
        return None
    else:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'button-merge' in changed_id:
            df_1 = pd.read_json(file_1_data, orient='split')
            df_2 = pd.read_json(file_2_data, orient='split')

            df_merged = pd.merge(df_1, df_2, left_on=str(radio_item_1), right_on=str(radio_item_2), how='inner')
            json_obj_merged = df_merged.to_json(date_format='iso', orient='split')

            return json_obj_merged

            # if selected_columns is not None:
            #     df_merged['Comparison Result'] = np.where(df_merged[selected_columns[0]] == df_merged[selected_columns[1]],
            #                                               'Match',
            #                                               'No Match')

        else:
            return None


@app.callback(Output('comparison-result', 'children'),
              Input('intermediate-value-comparison-result', 'data'),
             )
def show_merged_data(jsonified_data):
    if jsonified_data is not None:
        df_merged = pd.read_json(jsonified_data, orient='split')

        return dash_table.DataTable(
            id='dt-merged',
            data=df_merged.to_dict('records'),
            columns=[{'name': i, 'id': i, "selectable": True} for i in df_merged.columns],
            style_cell={'fontSize': 14, 'font-family': 'sans-serif'},
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="multi",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=15,
        )


@app.callback(
    Output('dt-merged', 'style_data_conditional'),
    Input('dt-merged', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]




@app.callback(Output('comparison-result2', 'children'),
              Input('intermediate-value-comparison-result', 'data'),
              Input('dt-merged', 'selected_columns')
             )
def add_compare_result(jsonified_data, selected_columns):
    if jsonified_data is not None :
        df_merged = pd.read_json(jsonified_data, orient='split')

        if selected_columns is not None:
            if len(selected_columns) == 2:
                df_merged['Comparison Result'] = np.where(df_merged[selected_columns[0]] == df_merged[selected_columns[1]],
                                                      'Match',
                                                      'No Match')
                return dash_table.DataTable(
                    id='dt-compared',
                    data=df_merged.to_dict('records'),
                    columns=[{'name': i, 'id': i, "selectable": True} for i in df_merged.columns],
                    style_cell={'fontSize': 14, 'font-family': 'sans-serif'},
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable=False,
                    row_deletable=False,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                    page_size=15,
                    export_format="csv"
                )


# --------------------------------------------------------------------------------------------------
# DB Comparison functions


@app.callback(
    Output('dd-output-table-1', 'children'),
    Input('dd-dropdown-1', 'value'),
)
def update_output(value_db_path):
    if value_db_path is not None:
        con_db1 = sl.connect(value_db_path)
        df_tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", con_db1)

        return html.Div([
            html.P("Table selection 1"),
            dcc.Dropdown(
                id='dd-dropdown-table-1',
                options=[
                    {'label': i, 'value': i} for i in df_tables['name']
                ]
            ),
            html.Div(id='dd-output-table-1')
        ])


@app.callback(
    Output('dd-output-table-2', 'children'),
    Input('dd-dropdown-2', 'value'),
)
def update_output(value_db_path):
    if value_db_path is not None:
        con_db1 = sl.connect(value_db_path)
        df_tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", con_db1)

        return html.Div([
            html.P("Table selection 2"),
            dcc.Dropdown(
                id='dd-dropdown-table-2',
                options=[
                    {'label': i, 'value': i} for i in df_tables['name']
                ]
            ),
            html.Div(id='dd-output-table-2')
        ])


@app.callback(
    Output('input-query', 'children'),
    Input('dd-dropdown-table-1', 'value'),
    Input('dd-dropdown-table-2', 'value'),
)
def create_query_text(table1, table2):
    if table1 is not None and table2 is not None:
        return html.Div([
            dbc.Textarea(
                id = 'input-query',
                className="mb-3",
                style={'width': '100%', 'height': 200},
                placeholder="Type your sql query here. Table1 and Table2 are the aliases to use"),
            dbc.Button(
                "Run Query",
                id="button-run-query",
                color="primary",
                disabled=False,
                n_clicks=0
            )
            ])


@app.callback(
    Output('output-query', 'children'),
    Input('dd-dropdown-1', 'value'),
    Input('dd-dropdown-2', 'value'),
    Input('dd-dropdown-table-1', 'value'),
    Input('dd-dropdown-table-2', 'value'),
    Input('input-query', 'value'),
    Input('button-run-query', 'n_clicks'),
)
def create_query_text(db1, db2, table1, table2, input_query, n_clicks):
    if db1 is not None and db2 is not None and table1 is not None and table2 is not None and input_query is not None:
        if n_clicks is None or n_clicks == 0:
            return None
        else:
            formatted_sql = sqlparse.format(input_query, reindent=True, keyword_case='upper')
            parser_result = Parser(formatted_sql)

            if parser_result is None:
                return None

            else:
                if parser_result.query_type == QueryType.SELECT:

                    fields = parser_result.columns_dict['select'][0]

                    tbl1_join_column = parser_result.columns_dict['join'][0].split('.')[1]
                    tbl2_join_column = parser_result.columns_dict['join'][1].split('.')[1]



                    for elm in parser_result.sqlparse_tokens:
                        if type(elm).__name__ == 'Comparison':
                            condition_elm = elm
                    if condition_elm is not None:
                        if "=" in condition_elm.value:
                            con_db1 = sl.connect(db1)
                            query1 = "SELECT " + str(fields) + " FROM " + str(table1)
                            df1 = pd.read_sql(query1, con_db1)

                            con_db2 = sl.connect(db2)
                            query2 = "SELECT " + str(fields) + " FROM " + str(table2)
                            df2 = pd.read_sql(query2, con_db2)

                            try:
                                df_merged = pd.merge(df1, df2, left_on=tbl1_join_column, right_on=tbl2_join_column,
                                                 how='inner')
                                if df_merged is None:
                                    return None
                                else:
                                    return dash_table.DataTable(
                                        id='output-query',
                                        data=df_merged.to_dict('records'),
                                        columns=[{'name': i, 'id': i, "selectable": True} for i in df_merged.columns],
                                        style_cell={'fontSize': 14, 'font-family': 'sans-serif'},
                                        editable=True,
                                        filter_action="native",
                                        sort_action="native",
                                        sort_mode="multi",
                                        column_selectable=False,
                                        row_deletable=False,
                                        selected_columns=[],
                                        selected_rows=[],
                                        page_action="native",
                                        page_current=0,
                                        page_size=15,
                                        export_format="csv"
                                    )

                            except KeyError:
                                return None;
                                # return html.P("Column referenced in join condition does not exist")


                        elif "<>" in condition_elm:
                            return html.P("Only equals = expressions are allowed")
                    else:
                        return html.P("Please add a join condition")
                else:
                    return html.P("Only select expressions are allowed")


if __name__ == "__main__":
    # Using real server
    host_url, host_port = ['localhost', 8081]
    print('http://' + host_url + ':' + str(host_port))
    from waitress import serve

    serve(app.server, host=host_url, port=host_port)

    # Using test server with debug on browser
    # app.run_server(debug=True)

    # Using server
    # app.run_server(debug=False)
