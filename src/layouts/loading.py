import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from layouts.loading_layout import navbar

##==================================
## Assemble layout
##==================================
out = [
    navbar.get(),
    html.Br(),
    dbc.Col(
        dbc.Spinner(color='primary', size = 'lg'),
        style = dict(textAlign = 'center')
    )
]

def layout():
    return out
