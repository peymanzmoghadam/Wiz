import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from layouts.global_layout import data_table
from layouts.lines_layout import app_navbar, top_row, graph, axis_select, sheet_slider, help_dialog
from functions.global_functions import genSession

##==================================
## Assemble layout
##==================================
out = [
    app_navbar.get(),
    top_row.get(),
    graph.get(),
    axis_select.get(),
    sheet_slider.get(),
    help_dialog.get(),
    data_table.get('lines'),
    html.Div(id='lines-session-id', style=dict(display='none')),
    html.Div(id='lines-graph-timestamp', style=dict(display='none')),
    html.Div(id='lines-table-timestamp', style=dict(display='none')),
    html.Div(id='lines-table-filter', style=dict(display='none')),
    html.Div(id='lines-table-selected-rows', style=dict(display='none')),
]

def layout():
    return out
