import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Axes selectors
##==================================
out = dbc.Col([
        dbc.Row([
                # Y-Axis Dropdown Selector
                html.Div([
                    dcc.Dropdown(
                        id='lines-y-select',
                        options = [],
                        placeholder = 'Select...',
                        clearable = True,
                        multi = True,
                    )
                ], className = 'dropdown-axis', style = dict(width = 400)
                ),
        ], justify = 'center', align = 'center'),
        dbc.Row([
            html.Div([
                html.P('x: ')
            ], className = 'dropdown-label'
            ),

            html.Div([
                dbc.RadioItems(
                    id = 'lines-x-axis-type',
                    options = [
                        dict(label = 'Linear' , value = 'linear'),
                        dict(label = 'Log', value = 'log')
                    ],
                    value = 'linear',
                    inline=True,
                )
            ], className = 'axis-type'
            ),

            html.Div([
                html.P('y: ')
            ], className = 'dropdown-label'
            ),


            html.Div([
                dbc.RadioItems(
                    id = 'lines-y-axis-type',
                    options = [
                        dict(label = 'Linear' , value = 'linear'),
                        dict(label = 'Log', value = 'log')
                    ],
                    value = 'linear',
                    inline=True,
                )
            ], className = 'axis-type'
            )

        ], justify = 'center'),
    ],
    id = 'lines-axis-dropdowns',
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
