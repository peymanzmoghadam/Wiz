import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app

help_content = [
    dcc.Markdown('''
## Usage

**Upload** data in the top left-hand side of the app. One Excel
file or multiple CSVs/DATs/TXTs are accepted. Data is read in as below.
    '''
    ),

    html.Img(src=app.get_asset_url('images/PCA_Help_Data.png'), style = dict(width = 400)),

    dcc.Markdown('''
If doing PCA, then **selecting** a class option will simply identify the classes in the plot.
PCA is unsupervised so the class selection is not necessary.

If doing LDA, the class is required to do analysis as it is a form of supervised learning.

**Slide** between sheets, or datafiles, with the slide feature at the bottom of the page.

**Filter** the data to plot using the Filter Data button.
The plot contains selected data or all rows if none are selected.
Filter arguments can be simple searches or inequalities (eg. < 60).
Download the plotted data in the navigation bar.
'''
    )
]


modal = html.Div(
    dbc.Modal(
    [
        dbc.ModalHeader(
            dbc.Button("Close", id="pca-help-close", className="ml-auto")
        ),
        dbc.ModalBody(help_content),
    ],
    id="pca-help-modal",
    size = 'lg',
    scrollable = True,
    ),
)


def get():
    return modal
