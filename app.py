import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

# Company list
company_list = {'AAPL': 'Apple', 'GOOG': 'Google', 'MSFT': 'Microsoft'}

app.layout = html.Div(children = [
    html.Div(children = '''
        Symbol to graph:
    '''),
    dcc.Dropdown(
        id = 'input',
        options = [
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Google', 'value': 'GOOG'},
            {'label': 'Microsoft', 'value': 'MSFT'}
        ],
        value = 'AAPL'
    ),
    html.Div(id = 'output-graph'),
])

@app.callback(
    Output(component_id = 'output-graph', component_property = 'children'),
    [Input(component_id = 'input', component_property = 'value')]
)
def update_value(company):
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(company, 'yahoo', start, end)
    df.reset_index(inplace = True)
    df.set_index("Date", inplace = True)

    return dcc.Graph(
        id = 'example-graph',
        figure = {
            'data': [
                {'x': df.index, 'y': df.Close, 'type': 'line', 'name': company},
            ],
            'layout': {
                'title': company_list[company]
            }
        }
    )

if __name__ == '__main__':
    app.run_server()
