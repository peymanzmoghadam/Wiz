import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Navigation bar
##==================================
download_link = html.A(
    'Download Plot Data',
    id = 'lines-download-link',
    href = '',
    style = dict(color = 'white'),
    className= 'downloadlink'
),

navbar = dbc.NavbarSimple(
    [
        dbc.Nav(
            dbc.Row(
                [
                    dbc.NavItem(dbc.NavLink('Clear Data',id='clear-data-link',href='/temp-clear')),
                    dbc.NavItem(dbc.NavLink(download_link),id='lines-dowload-nav'),
                    dbc.NavItem(dbc.NavLink('Data Table',id='lines-table-open'), style = dict(cursor = 'pointer')),
                    dbc.NavItem(dbc.NavLink('PCA/LDA', href='/pca')),
                 ],
                 align = 'center',
                 no_gutters = True,
            ),
        ),
    ],
    brand = '   ',
    brand_href = '/',
    expand = 'lg',
    color="primary",
    id='navBar',
    light = False,
    dark = True,
)

def get():
    return navbar
