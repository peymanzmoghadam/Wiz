import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def get(id):
    table_content = html.Div(
        [
            dt.DataTable(
                id = id + '-data-table',
                data = [{}],
            )
        ],

        className = 'data-table-container',
        id = id + '-table-container',
    )

    modal = html.Div([
        dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.Button("Close", id=id + "-table-close", className="ml-auto")
            ),
            dbc.ModalBody(table_content),
        ],
        id= id + "-table-modal",
        size = 'lg',
        scrollable = True,
        backdrop='static',
        is_open = True # This ensures that the table will render (will close modal on page loading)
        ),
    ])
    return modal

def get_table(id):
    return html.Div([
            dt.DataTable(
                id = id,
                data = [{}],
            )
        ],

        className = 'data-table-container',
        id = id + '-container',
        style = dict(display = 'none')
    )
