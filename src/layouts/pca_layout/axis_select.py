import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Selectors
##==================================
out = dbc.Col([
        dbc.Row([
            # Class selector (what differentiates the data)
            dbc.Col([
                html.Div([
                    html.P('Classes:    ')
                ], className = 'dropdown-label', style = dict(marginRight = 30)
                ),

                html.Div([
                    dcc.Dropdown(
                        id='pca-class-select',
                        options = [],
                        placeholder = 'Select...',
                        clearable = True,
                    )
                ], className = 'dropdown-axis'
                ),

            ], className = 'dropdown-group'
            ),
        ], justify = 'center'),
    ],
    id = 'pca-axis-dropdowns',
    width = dict(size = 12, offset = 0),
    style = dict(
        marginTop = 30,
        marginLeft = 0,
        marginRight = 0,
    ),
    align = 'center',
)

def get():
    return out
