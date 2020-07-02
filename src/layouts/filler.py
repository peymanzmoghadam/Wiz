import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Welcome message
##==================================
message = dbc.Col(
    html.H3(['No page here! Please return to the ', dcc.Link('homepage.', href = '/')], style = dict(textAlign='center')),
    width = dict(size = 8, offset = 2),
)

navbar = dbc.NavbarSimple(
    [
        dbc.Nav(
            dbc.Row(
                [
                    # Navigation
                    dbc.NavItem(dbc.NavLink('Lines', href='/')),
                    dbc.NavItem(dbc.NavLink('PCA/LDA', href='/pca')),
                 ],
                 align="center",
                 no_gutters=True,
            ),
        fill = True
        ),
    ],
    brand='  ',
    brand_href="#",
    color="primary",
    id='navBar',
    light = False,
    dark = True,
)

##==================================
## Assemble layout
##==================================
out = [
    navbar,
    html.Br(),
    message,
]

def layout():
    return out
