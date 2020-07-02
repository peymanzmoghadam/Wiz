import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Navigation bar
##==================================
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

def get():
    return navbar
