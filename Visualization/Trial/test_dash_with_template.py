from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

# We set template folder as one directory above in Templates.
# If code and templates are in the same folder no need to set template_folder
app = Flask(__name__, template_folder='../Templates')


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))


@app.route('/')
def index():
    return render_template('chartsajax.html', graphJSON=gm())


def gm(country='United Kingdom'):
    df = pd.DataFrame(px.data.gapminder())

    fig = px.line(df[df['country'] == country], x="year", y="gdpPercap")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == '__main__':
    app.run(debug=True)
