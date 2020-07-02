import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Upload component
##==================================
upload = dbc.Col([
    dcc.Loading(
        dcc.Upload(
            html.H6([
                'Drag and Drop or ',
                html.A('Select a File')
            ]),
            style_active = dict(
                borderStyle = 'solid',
                borderColor = '#0FA0CE',
                backgroundColor = '#eee',
                ),
            multiple = True,
            loading_state = dict(
                is_loading = False,
            ),
            id = 'lines-file-upload',
            className = 'upload',
        ),
        id="lines-loading-upload",
        fullscreen=False,
    ),
    ],
    id = 'lines-upload',
    style = dict(zIndex = 1001),
    width = dict(size = 3, offset = 1),
    align = 'center'
)

##==================================
## Graph type selector
##==================================
# Label
radio_label = html.H6('Input Data Type:', style = dict(marginRight = 7))

# Radio buttons
radios = dbc.FormGroup(
    [
        dbc.RadioItems(
            id = 'lines-data-type',
            options=[
                {"label": "Type 1", "value": 1},
                {"label": "Type 2", "value": 2},
            ],
            value=1,
            inline=True,
        ),
    ]
)


radio_select = dbc.Col(
    [
        dbc.Row(
            [
                radio_label,
                radios
            ],
            justify = 'center'
        )
    ],
    id = 'lines-radio-container', width = 4, align = 'end'
)


##==================================
## Assemble layout
##==================================
output = dbc.Row(
    [
        upload,
        radio_select
    ],
    justify = 'between',
    align = 'center',
    style = dict(marginTop = 5, marginBottom = 10)
)



def get():
    return output
