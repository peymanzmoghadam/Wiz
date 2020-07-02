import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

out_graph = dcc.Graph(
    id = 'lines-graph',
    config = dict(
        displayModeBar = False,
    ),
    figure = dict(
        data = [],
        layout = go.Layout(
            xaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False
            ),
            yaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False
            )
        )
    ),
    style = dict(
        height = '100%',
    )
)

# Draw starting graph
out = html.Div(
    [
        out_graph
    ],
    id ='lines-graph-container'
)


def get():
    return out

def get_graph():
    return out_graph
