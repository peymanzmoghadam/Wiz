##==================================
## External imports
##==================================
import datetime
import pandas as pd
import numpy as np
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

##==================================
## Internal imports
##==================================
from app import app
from functions.global_functions import *
from functions.pca.data import *
from functions.pca.graph import *
from layouts.pca_layout import graph


##==================================
## Callbacks
##==================================
# Upload data and create data slider
@app.callback(
    [
        Output('pca-slider','marks'),
        Output('pca-slider','min'),
        Output('pca-slider','max'),
        Output('pca-loading-upload', 'children'),
        Output('pca-graph-container','children'),
        Output('pca-session-id','children'),
    ],
    [
        Input('pca-file-upload','contents'),
        Input('pca-file-upload','filename'),
    ],
    [
        State('pca-session-id','children'),
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
        id            = 'pca-file-upload',
        className     = 'upload',
        disabled      = True,
        contents      = None
    )

    return slider_out, slider_min, slider_max, out, graph.get_graph(), session_id

## Populate dropdowns
@app.callback(
    [
        Output('pca-class-select','options'),
        Output('pca-class-select','value'),
    ],
    [
        Input('pca-slider','value'),
        Input('pca-analysis-type','value'),
        Input('pca-session-id','children'),
    ],
    [

        State('pca-file-upload','contents'),
        State('pca-file-upload','filename'),
        State('pca-class-select','value'),
    ],
    prevent_initial_call = True,
)
def populate_dropdowns(sheet_num, analysis_type, session_id, file_contents, file_name, class_value):
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

        if 'pca-analysis-type' in trigger_id:
            get_value = False

    # Load data
    data = get_data(session_id, file_contents, file_name)

    # Get the name of the sheet
    sheet = list(data)[sheet_num]

    # Get data from the specified sheet
    sub_data = data[sheet]

    # Get labels
    class_labels = get_labels(sub_data)
    options = [{'label': i, 'value': i} for i in class_labels]

    # If the new options have the previous value, then set it
    if class_value in [item['label'] for item in options]:
        class_out = class_value;
    else:
        class_out = None

    # LDA requires classes
    if class_out is None and analysis_type == 2:
        class_out = options[0]['value']

    return options, class_out

@app.callback(
    [
        Output('pca-graph','figure'),
        Output('pca-graph','style'),
        Output('pca-graph','config'),
        Output('pca-graph-2','figure'),
        Output('pca-graph-2','style'),
        Output('pca-graph-2','config'),
        Output('pca-graph-timestamp','children'),
    ],
    [
        Input('pca-class-select','value'),
        Input('pca-graph','clickData'),
        Input('pca-analysis-type','value'),
        Input('pca-data-table','filter_query'),
    ],
    [
        State('pca-slider','value'),
        State('pca-graph-timestamp','children'),
        State('pca-session-id','children'),
        State('pca-file-upload','contents'),
        State('pca-file-upload','filename'),
        State('pca-table-filter','children'),
    ],
    prevent_initial_call = True
)
def update_PCA_graph(class_select, click_data, analysis_type, filter_query,
    sheet_num, graph_timestamp, session_id, file_contents, file_name, prev_filter_query):
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
        full_id = ctx.triggered[0]['prop_id']
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        prop_id = ctx.triggered[0]['prop_id'].split('.')[1]

        # Don't update if the selected rows did not change didn't change (table 1)
        if filter_query is None:
            filter_query = ''
        if prev_filter_query is None:
            prev_filter_query = ''
        if 'filter_query' in full_id and filter_query in prev_filter_query:
            if not filter_query and not prev_filter_query1:
                raise PreventUpdate

        # If the click data does not trigger, that means the graph is changing (get rid of click data)
        # If click data is the only thing updated, then don't update the timestamp
        if 'pca-graph' not in trigger_id:
            click_data = None
        else:
            date_out = graph_timestamp

        # Don't update the timestamp if only filtering or row-select is occuring
        if 'pca-data-table' in trigger_id:
            date_out = graph_timestamp

    # Get the data
    data = get_data(session_id, file_contents, file_name)

    # Get the name of the sheet
    sheet = list(data)[sheet_num]

    # Get data from the specified sheet
    plot_data = data[sheet]

    # Pickle the dataset
    pickleData(plot_data, session_id)

    # Filter the dataset
    plot_data = filter_data(plot_data, filter_query, [], [])

    # Do analysis and plot based on the input type
    if analysis_type == 1:
        # Analysis
        Y, var_exp, cum_var_exp = PCA(plot_data, class_select)

        # Get figures
        out_style, out_figure, animate = PCA_plot(Y, plot_data, var_exp, cum_var_exp, class_select, click_data)
        out_style_2, out_figure_2 = PCA_plot_2(var_exp, cum_var_exp)

    else:
        # Analysis
        Y_lda, var_exp, cum_var_exp = LDA(plot_data, class_select)

        # Determine figure type from data
        out_style, out_figure, animate = LDA_plot(Y_lda, plot_data, var_exp, cum_var_exp, class_select)
        out_style_2, out_figure_2 = LDA_plot_2(var_exp, cum_var_exp)

    # Configuration for figure
    if len(list(plot_data)) < 1:
        value = False
    else:
        value = 'hover'
    configure_graph = graph_configure(value)

    out =[
            dcc.Graph(
                id = 'pca-graph',
                config = configure_graph,
                figure = out_figure,
                style = out_style
            ),
            dcc.Graph(
                id = 'pca-graph-2',
                config = configure_graph,
                figure = out_figure_2,
                style = out_style_2
            )
        ]

    return out_figure, out_style, configure_graph, out_figure_2, out_style_2, configure_graph, date_out

# Make data tables
@app.callback(
    [
        Output('pca-table-container','children'),
        Output('pca-table-timestamp','children'),
    ],
    [
        Input('pca-table-open', 'n_clicks'),
        Input('pca-data-table','page_current'),
        Input('pca-data-table','filter_query'),
    ],
    [
        State('pca-table-timestamp','children'),
        State('pca-graph-timestamp','children'),
        State('pca-session-id','children'),
        State('pca-analysis-type','value'),
    ],
    prevent_initial_call = True
)
def update_tables(n_clicks_open, page_current, filter_query,
    table_timestamp, graph_timestamp, session_id, analysis_type):
    # Don't update if there is no session ID
    if session_id is None:
        return empty_table('pca-data-table'), table_timestamp

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
        if 'pca-table-open' in trigger_id:
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
            date_out = table_timestamp

    # Get the sub data used for plotting
    plot_data = unpickleData(session_id)

    # Process inputs that may not be set
    if filter_query is None:
        filter_query = ''
    if page_current is None:
        page_current = 0

    # Get the data to display and properties of the table
    table_data, page_size, page_count, columns = backend_table(plot_data, filter_query, [], page_current)

    # Get table styling
    css, style_table, style_cell = data_table_style()

    # Build output table
    table = dt.DataTable(
        id             = 'pca-data-table',
        data           = table_data,
        columns        = columns,

        page_action    = 'custom',
        page_current   = page_current,
        page_size      = page_size,
        page_count     = page_count,

        filter_action  = 'custom',
        filter_query   = filter_query,

        editable       = False,
        row_deletable  = False,

        css            = css,
        style_table    = style_table,
        style_cell     = style_cell
    )

    return table, date_out

# Update download link for plotted data
@app.callback(
    Output('pca-download-link','href'),
    [
        Input('pca-session-id','children'),
        Input('pca-graph-timestamp','children')
    ],
    [
        State('pca-class-select','value'),
        State('pca-analysis-type','value'),
        State('pca-data-table','filter_query')
    ],
    prevent_initial_call = True
)
def update_download_link(session_id, time_stamp, class_select, analysis_type, filter_query):
    # Unpickle data
    plot_data = unpickleData(session_id)

    # Filter the data
    plot_data = filter_data(plot_data, filter_query, [], [])

    # Do analysis and plot based on the input type
    if analysis_type == 1:
        # Analysis
        Y, var_exp, cum_var_exp = PCA(plot_data, class_select)
        type = 'PC'
    else:
        # Analysis
        Y, var_exp, cum_var_exp = LDA(plot_data, class_select)
        type = 'LD'

    # Create data frame
    n = len(var_exp)
    df = pd.DataFrame(Y, columns = [type + ' %s' %i for i in range(1, n+1)]);

    temp = np.array([var_exp, cum_var_exp])
    df1 = pd.DataFrame({'Individual': var_exp, 'Cumulative': cum_var_exp})

    # Combine dataframes
    dff = pd.concat([df,df1], axis=1)

    # Pickle the dataframe
    pickleData(dff, session_id + 'analysis')

    # Store the proper url
    return '/' + CACHE_DIRECTORY + '?value={}'.format(session_id + 'analysis')

# Help modal
@app.callback(
    Output('pca-help-modal', 'is_open'),
    [
        Input('pca-help-close', 'n_clicks'),
        Input('pca-help-open', 'n_clicks'),
    ],
    [
        State('pca-help-modal','is_open')
    ],
    prevent_initial_call = True,
)
def help_modal(n_clicks_close, n_clicks_open, is_open):
    if n_clicks_open or n_clicks_close:
        return not is_open
    return is_open

# Data table modal (closes modal on initial callback - tricky but necessary!)
@app.callback(
    Output('pca-table-modal', 'is_open'),
    [
        Input('pca-table-close', 'n_clicks'),
        Input('pca-table-open', 'n_clicks'),
    ],
    [
        State('pca-table-modal','is_open')
    ],
)
def table_modal(n_clicks_close, n_clicks_open, is_open):
    return not is_open
