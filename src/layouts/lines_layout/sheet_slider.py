import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Slider
##==================================
out = dbc.Col(
    [
        html.Div(
            [
                dcc.Slider(
                    id = 'lines-slider',
                    min = 0,
                    max = 0,
                    marks = {},
                    value = 0,
                    updatemode = 'drag'
                    )
            ],
            id = 'lines-slider-call',
            className = 'slider'
        )
    ],
    width = dict(size = 6, offset = 3),
    id = 'lines-filter-slider'
)

def get():
    return out
