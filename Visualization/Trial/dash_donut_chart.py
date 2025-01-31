# Donut chart plotting without callbacks. No reactions, only plotting

import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go

labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
values = [4500, 2500, 1053, 500]

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

# if __name__ == "__main__":
#     from waitress import serve
#     serve(app.server, host="0.0.0.0", port=8081)