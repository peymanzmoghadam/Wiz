##==================================
## External imports
##==================================
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import datetime

##==================================
## Internal imports
##==================================
from app import app
from functions.global_functions import *
from functions.lines.data import *
from functions.lines.graph import *
from layouts.lines_layout import graph

##==================================
## Callbacks
##==================================
# Upload data and create data slider
@app.callback(
    [
        Output('lines-slider','marks'),
        Output('lines-slider','min'),
        Output('lines-slider','max'),
        Output('lines-slider','value'),
        Output('lines-loading-upload', 'children'),
        Output('lines-graph-container','children'),
        Output('lines-session-id','children'),
    ],
    [
        Input('lines-file-upload','contents'),
        Input('lines-file-upload','filename'),
    ],
    [
        State('lines-session-id','children'),
    ],
    prevent_initial_call = True,
)
def process_data_upload(file_contents, file_name, session_id):
    # Don't update if there is no data
    if file_contents is None:
        raise PreventUpdate

    # Get a new session ID for the new file
    session_id = genSession()

    # Get the uploaded data
    all_data = get_data(session_id, file_contents, file_name)

    # Populate the slider bar with the sheet options
    sheets = list(all_data)
    slider_out = {i : sheets[i] for i in range(len(sheets))}
    slider_min = 0
    slider_max = len(sheets) - 1

    # Delete oldest cache if it is accumulating
    path = os.getcwd() + '/' + CACHE_DIRECTORY + '/'
    delete_cache(path)

    out = dcc.Upload(
        html.H6(
        'Clear previous data to upload again'),
        style_active  = dict(
            borderStyle     = 'solid',
            borderColor     = '#0FA0CE',
            backgroundColor = '#eee',
        ),
        multiple      = True,
        loading_state = dict(
            is_loading = False,
        ),
        id            = 'lines-file-upload',
        className     = 'upload',
        disabled      = True,
        contents      = None
    )

    return slider_out, slider_min, slider_max, slider_min, out, graph.get_graph(), session_id

# Populate dropdowns
@app.callback(
    [
        Output('lines-y-select','options'),
        Output('lines-y-select','value'),
    ],
    [
        Input('lines-slider','value'),
        Input('lines-data-type','value')
    ],
    [
        State('lines-session-id','children'),
        State('lines-file-upload','contents'),
        State('lines-file-upload','filename'),
        State('lines-y-select','value'),
    ],
    prevent_initial_call = True,
)
def populate_dropdowns(sheet_num, datatype, session_id, file_contents, file_name, y_value):
    # Don't update if there is no session ID
    if session_id is None:
        raise PreventUpdate

    # Default value for callback
    get_value = True

    # Get info on what triggered the callback
    ctx = dash.callback_context

    # Do any necessary processing on the callback triggers
    if not ctx.triggered:
        trigger_id = None
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        prop_id = ctx.triggered[0]['prop_id'].split('.')[1]

        if 'lines-data-type' in trigger_id:
            get_value = False

    # Load data
    data = get_data(session_id, file_contents, file_name)

    # Get the name of the sheet
    sheet = list(data)[sheet_num]

    # Get data from the specified sheet
    sub_data = data[sheet]

    # Get labels
    x_labels, y_labels, size_labels = get_labels(sub_data, datatype)

    # Set options
    options = [{'label': i, 'value': i} for i in size_labels]
    size_options = [{'label': i, 'value': i} for i in size_labels]
    y = options;

    # Either keep the same y-selections or clear the dropdown selection
    if get_value:
        if y_value is None:
            if y_value in [item['label'] for item in options]:
                y_out = y_value
            else:
                y_out = None
        else:
            y_out = []
            for y_i in y_value:
                if y_i in [item['label'] for item in options]:
                    y_out.append(y_i)
                else:
                    y_out = None
    else:
        y_out = None

    return y, y_out

# Callback to update graph
@app.callback(
    [
        Output('lines-graph','figure'),
        Output('lines-graph','style'),
        Output('lines-graph','animate'),
        Output('lines-graph','config'),
        Output('lines-graph-timestamp','children'),
        Output('lines-table-filter','children'),
        Output('lines-table-selected-rows','children'),
    ],
    [
        Input('lines-y-select','value'),
        Input('lines-x-axis-type','value'),
        Input('lines-y-axis-type','value'),
        Input('lines-graph','clickData'),
        Input('lines-data-table','filter_query'),
        Input('lines-data-table','selected_rows'),
    ],
    [
        State('lines-data-table','sort_by'),
        State('lines-graph-timestamp','children'),
        State('lines-slider','value'),
        State('lines-data-type','value'),
        State('lines-session-id','children'),
        State('lines-file-upload','contents'),
        State('lines-file-upload','filename'),
        State('lines-table-filter','children'),
        State('lines-table-selected-rows','children'),
    ],
    prevent_initial_call = True,
)
def update_graph(y_column, x_type, y_type, click_data, filter_query,
    selected_rows, sort_by, graph_timestamp, sheet_num, data_type,  session_id, file_contents, file_name,
    prev_filter_query, prev_selected_rows):
    # Don't update if there is no session ID
    if session_id is None:
        raise PreventUpdate

    # Set the current time for output
    date_out = datetime.datetime.now()

    # Get info on what triggered the callback
    ctx = dash.callback_context

    # Do any necessary processing on the callback triggers
    if not ctx.triggered:
        trigger_id = None
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        prop_id = ctx.triggered[0]['prop_id'].split('.')[1]

        # Don't update if the selected rows did not change didn't change
        if filter_query is None:
            filter_query = ''
        if prev_filter_query is None:
            prev_filter_query = ''
        if selected_rows is None:
            selected_rows = []
        if prev_selected_rows is None:
            prev_selected_rows = []
        if 'filter_query' in prop_id and selected_rows != []:
            selected_rows = []
            prev_selected_rows = []
            raise PreventUpdate
        if 'filter_query' in prop_id and filter_query in prev_filter_query:
            if not filter_query and not prev_filter_query:
                raise PreventUpdate
        if 'selected_rows' in prop_id and selected_rows is prev_selected_rows:
            raise PreventUpdate

        # If the click data does not trigger, that means the graph is changing (get rid of click data)
        # If click data is the only thing updated, then don't update the timestamp
        if 'lines-graph' not in trigger_id:
            click_data = None
        else:
            date_out = graph_timestamp

        # Don't update the timestamp if only filtering or row-select is occuring
        if 'lines-data-table' in trigger_id:
            date_out = graph_timestamp

    # Return default is there is nothing selected
    if y_column is None or y_column == []:
        return dict(data = [], layout = blank_layout()), dict(height = '100%', width = '100%'), False, graph_configure(False), date_out, None, None

    # Get the data
    data = get_data(session_id, file_contents, file_name)

    # Get the name of the sheet
    sheet = list(data)[sheet_num]

    # Get data from the specified sheet
    sub_data = data[sheet]

    # Reduce the data to only what is needed to plot
    plot_data = get_plot_data(sub_data, y_column, data_type)
    columns = list(plot_data)

    # Pickle the plot data for other processes to use
    pickleData(plot_data,session_id)

    # Filter the data based on filtering in the data table
    plot_data = filter_data(plot_data, filter_query, sort_by, selected_rows)

    # Determine figure type from data
    out_style, out_figure, animate = pick_plot(plot_data, columns, click_data, x_type, y_type, data_type)

    # Configuration for figure
    if len(columns) > 1:
        configure_graph = graph_configure('hover')
    else:
        configure_graph = graph_configure(False)

    return out_figure, out_style, animate, configure_graph, date_out, filter_query, selected_rows

# Make data table
@app.callback(
    [
        Output('lines-table-container','children'),
        Output('lines-table-timestamp','children'),
    ],
    [
        Input('lines-table-open', 'n_clicks'),
        Input('lines-data-table','page_current'),
        Input('lines-data-table','sort_by'),
        Input('lines-data-table','filter_query'),
    ],
    [
        State('lines-data-table','selected_rows'),
        State('lines-table-timestamp','children'),
        State('lines-graph-timestamp','children'),
        State('lines-session-id','children'),
        State('lines-data-type','value'),
        State('lines-y-select','value')
    ],
    prevent_initial_call = True,
)
def update_table(n_clicks_open, page_current, sort_by, filter_query, selected_rows, table_timestamp, graph_timestamp, session_id, data_type, y_column):
    # Don't update if there is no session ID
    if session_id is None:
        raise PreventUpdate

    # Set the current time for output
    date_out = datetime.datetime.now()

    # Get info on what triggered the callback
    ctx = dash.callback_context

    # Do any necessary processing on the callback triggers
    if not ctx.triggered:
        trigger_id = None
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        prop_id    = ctx.triggered[0]['prop_id'].split('.')[1]

        # Controls for when the "open" button opened the table
        if 'lines-table-open' in trigger_id:
            # Don't update the table if the graph hasn't updated
            if table_timestamp is not None:
                if graph_timestamp is None:
                    raise PreventUpdate
                if table_timestamp > graph_timestamp:
                    raise PreventUpdate

        # Controls for when a table property was changed
        if 'page_current' in prop_id:
            date_out = table_timestamp
        if 'sort_by' in prop_id:
            date_out = table_timestamp
        if 'filter_query' in prop_id:
            selected_rows = []
            date_out = table_timestamp

    # Return default if nothing is selected
    if y_column is None or y_column == []:
        return empty_table('lines-data-table'), table_timestamp

    # Get the plotted data from unpickling it
    plot_data = unpickleData(session_id)

    # Process inputs that may not be set
    if selected_rows is None:
        selected_rows = []
    if filter_query is None:
        filter_query = ''
    if sort_by is None:
        sort_by = []
    if page_current is None:
        page_current = 0

    # Get the data to display and properties of the table
    table_data, page_size, page_count, columns = backend_table(plot_data, filter_query, sort_by, page_current)

    # Get table styling
    css, style_table, style_cell = data_table_style()

    # Build output table
    table = dt.DataTable(
        id             = 'lines-data-table',
        data           = table_data,
        columns        = columns,

        page_action    = 'custom',
        page_current   = page_current,
        page_size      = page_size,
        page_count     = page_count,

        row_selectable = "multi",
        selected_rows  = selected_rows,

        sort_action    = 'custom',
        sort_mode      = 'single',
        sort_by        = sort_by,
        filter_action  = 'custom',
        filter_query   = filter_query,

        editable       = False,
        row_deletable  = False,

        css            = css,
        style_table    = style_table,
        style_cell     = style_cell
    )

    # If the data is type 2, then turn off data filtering, sorting, or selecting.
    if data_type == 2:
        table = dt.DataTable(
            id             = 'lines-data-table',
            data           = table_data,
            columns        = columns,

            page_action    = 'custom',
            page_current   = page_current,
            page_size      = page_size,
            page_count     = page_count,

            row_selectable = False,

            sort_action    = 'none',
            filter_action  = 'none',

            editable       = False,
            row_deletable  = False,

            css            = css,
            style_table    = style_table,
            style_cell     = style_cell
        )
    return table, date_out


# Update download link for plotted data
@app.callback(
    Output('lines-download-link','href'),
    [
        Input('lines-session-id','children')
    ],
    prevent_initial_call = True
)
def update_download_link(sessionID):
    return '/' + CACHE_DIRECTORY + '?value={}'.format(sessionID)


# Help modal
@app.callback(
    Output('lines-help-modal', 'is_open'),
    [
        Input('lines-help-close', 'n_clicks'),
        Input('lines-help-open', 'n_clicks'),
    ],
    [
        State('lines-help-modal','is_open')
    ],
    prevent_initial_call = True,
)
def help_modal(n_clicks_close, n_clicks_open, is_open):
    if n_clicks_open or n_clicks_close:
        return not is_open
    return is_open

# Data table modal (closes modal on initial callback - tricky but necessary!)
@app.callback(
    Output('lines-table-modal', 'is_open'),
    [
        Input('lines-table-close', 'n_clicks'),
        Input('lines-table-open', 'n_clicks'),
    ],
    [
        State('lines-table-modal','is_open')
    ],
)
def table_modal(n_clicks_close, n_clicks_open, is_open):
    return not is_open
