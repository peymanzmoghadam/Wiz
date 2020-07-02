##==================================
## External imports
##==================================
import os
import io
import flask
import urllib
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

##==================================
## Internal imports
##==================================
# Import app and cache
from app import app, cache

# Import all layouts
from layouts import loading, filler, lines, pca

# Import callbacks for individual app pages
from callbacks import lines_call, pca_call

# Import functions
from functions.global_functions import unpickleData

##==================================
## Initialize app layout
##==================================
def serve_layout():
    return html.Div([
            html.Div(
                loading.layout(),
                id = 'page-content'
            ),
            dcc.Location(id='url', refresh = False),
        ]
    )
app.layout = serve_layout()
##==========================================
## Callbacks to determine layout based on url
##===========================================
@app.callback(
    Output('page-content', 'children'),
    [
        Input('url', 'pathname'),
    ],
)
def display_page(pathname):

    # Direct user to correct layout (page)
    if pathname == '/':
        return lines.layout()
    elif pathname == '/pca':
        return pca.layout()
    elif pathname is not None and 'temp' in pathname:
        return loading.layout()
    else:
        return filler.layout()

##==========================================
## Callbacks for clearing data
##===========================================
@app.callback(
    Output('url', 'pathname'),
    [
        Input('clear-data-link', 'n_clicks'),
    ],
    [
        State('url','pathname')
    ],
    prevent_initial_call=True
)
def clean_refresh(n_clicks, temp_pathname):
    # Prevent updates
    if n_clicks is None:
        raise PreventUpdate

    if temp_pathname is None:
        raise PreventUpdate

    # Update the URL to clear the page
    return temp_pathname

##==========================================
## Callback for downloading data
##===========================================
@app.server.route('/._cache-directory/')
def download_csv():
    # Get the session ID when requested
    session_id = flask.request.args.get('value')

    # Unpickle the data based on the sessionID
    data = unpickleData(session_id)

    # Use string IO to make CSV for output
    str_io = io.StringIO()
    data.to_csv(str_io, index=False)
    mem = io.BytesIO()
    mem.write(str_io.getvalue().encode('utf-8'))
    mem.seek(0)
    str_io.close()

    return flask.send_file(mem,
                           mimetype = 'text/csv',
                           attachment_filename = 'data.csv',
                           as_attachment = True)

##==========================================
## Calling index.py
##===========================================
if __name__ == '__main__':
    # Serve app from specified port
    app.run_server(host='0.0.0.0', port = 5115, debug = False)
