##==================================
## External imports
##==================================
import os
import base64
import io
from math import log10
import pandas as pd
import json
import urllib
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import uuid
import pickle

##==================================
## Internal imports
##==================================
from app import cache

##==================================
## Global variables
##==================================
# Plots
COLORSCALE = 'Viridis'
TEMPLATE = 'plotly_white'

FONT_FAMILY = dict(
    plot = 'Arial',
    plot_labels = 'Arial'
    )
FONT_SIZE = dict(
    plot = 18,
    plot_labels = 24
    )

AXIS_LINE_WIDTH = 2
AXIS_LINE_COLOR = 'black'

OPACITY = 0.8
DEFAULT_BUBBLE_SIZE = 25
MIN_BUBBLE_SIZE = 10
MAX_BUBBLE_SIZE = 40

WEBGL_CUTOFF = 7500
MAX_CAT_INTS = 20


TABLE_PAGE_SIZE = 50
FILTER_OPERATORS = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

MAX_CACHE_FILES = 50
CACHE_DIRECTORY = '._cache-directory'
##==================================
## Data upload/storage
##==================================
# Generate session ID
def genSession():
    return str(uuid.uuid1())

# Get data using caching
def get_data(session_id, contents, filename):
    @cache.memoize()
    def query_and_serialize_data(session_id):
        # Get the data from the uploaded
        return input_to_df(contents, filename)
    return query_and_serialize_data(session_id)

# Delete cache if it starts to build up
#   If the app is running long enough, the cache will automatically time out. This
#   is only for situations where you are using the app offline
def delete_cache(path):
    # Current files in cache directory
    files = os.listdir(path)

    # Get all of the files in path
    paths = [os.path.join(path, basename) for basename in files]

    # Delete the oldest files to keep the cache directory light
    while len(paths) > MAX_CACHE_FILES:
        oldest_file = min(paths, key=os.path.getctime)
        os.remove(oldest_file)
        paths = [os.path.join(path, basename) for basename in os.listdir(path)]
    return

# Transform input data from Dash upload into a dictionary of dataframes
def input_to_df(contents, filename):
    # Text-like data types
    data_types = ['.csv', '.dat','.txt']
    spreadsheet_types = ['.xls','.ods']

    # Allow .csv, .xls or .xlsx files
    if any(ext in filename[0] for ext in data_types):
        # Initialize filenames and output data type
        sheets = []
        df = dict()

        for i in range(len(filename)):
            # Add file as if it were a sheet
            for data_type in data_types:
                if data_type in filename[i]:
                    sheets.append(filename[i].split('.')[0])

            # Get info on file
            contents_type, content_string = contents[i].split(',')
            decoded = base64.b64decode(content_string)

            # Add dataframe to dict with filename as key
            df_temp = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            # Add to list
            df[sheets[i]] = df_temp

    elif any(ext in filename[0] for ext in spreadsheet_types):
        # Get file info
        contents_type, content_string = contents[0].split(',')
        decoded = base64.b64decode(content_string)

        # Read in file
        if 'ods' in filename[0]:
            df= pd.read_excel(io.BytesIO(decoded), sheet_name = None, engine = 'odf')
        else:
            df= pd.read_excel(io.BytesIO(decoded), sheet_name = None)

    else:
        df = dict()

    return df

# Pickle the plotted data and store with the sessionID
def pickleData(data, session_id):
    filename = CACHE_DIRECTORY + '/' + session_id
    with open(filename, 'wb') as file:
        pickle.dump(data, file, protocol = pickle.HIGHEST_PROTOCOL)

# Unpickle the data based on the sessionID
def unpickleData(session_id):
    filename = CACHE_DIRECTORY + '/' + session_id
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data
    
##==================================
## Manipulate dataframes
##==================================
# Get the column names from the data table
def get_columns(dt_columns):
    columns = [];
    for item in dt_columns:
        columns.append(item['name'])
    return columns

# Reformat column names for data table and plotting (can't have the same name for two columns)
def unique_columns(df):
    df_columns = df.columns
    new_columns = []
    for item in df_columns:
        counter = 0
        newitem = item
        while newitem in new_columns:
            counter += 1
            newitem = '{} [{}]'.format(item, counter)
        new_columns.append(newitem)
    df.columns = new_columns
    return df

# Reverse the unique columns
def ununique_columns(df):
    df_columns = df.columns
    new_columns = []
    for item in df_columns:
        if item.rfind('[') != -1:
            new_columns.append(item[:item.rfind('[')])
        else:
            new_columns.append(item)
    df.columns = new_columns
    return df

# Normalize the size of the bubbles in the plot
def normalize_size(size_data):
    # Bubble size range
    min_size = MIN_BUBBLE_SIZE; # Based on diameter size method
    max_size = MAX_BUBBLE_SIZE;
    max_data = max(size_data);
    min_data = min(size_data);

    # Uniform size if there are NaNs or if
    if max_data == min_data or size_data.isnull().values.any():
        size_data.fillna(0.0, inplace = True)
        norm_size_data = size_data * 0.0 + DEFAULT_BUBBLE_SIZE
    else:
        norm_size_data = (max_size - min_size)/(max_data - min_data)*(size_data - min_data) + min_size
    return norm_size_data

# Maximum and minimum size for size axis label
def format_size(sizes):
    min_size = ''
    max_size = ''
    if sizes is not None:
        # Format outputs
        if sizes[0] > 100:
            min_size = "{:.0f}".format(sizes[0])
        elif sizes[0] > 10:
            min_size = "{:.1f}".format(sizes[0])
        elif sizes[0] > 1:
            min_size = "{:.2f}".format(sizes[0])
        else:
            min_size = "{:.3f}".format(sizes[0])

        if sizes[1] > 100:
            max_size = "{:.0f}".format(sizes[1])
        elif sizes[1] > 10:
            max_size = "{:.1f}".format(sizes[1])
        elif sizes[1] > 1:
            max_size = "{:.2f}".format(sizes[1])
        else:
            max_size = "{:.3f}".format(sizes[1])

        output = [min_size, max_size]

    else:
        output = [None, None]

    return output

##==================================
## Filtering/sorting functions
##==================================
def split_filter_part(filter_part):
    for operator_type in FILTER_OPERATORS:
        for operator in operator_type:
            if operator in filter_part:
                # Get the name of the column first
                name_part = filter_part.split('}')[0] + '}'
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                if operator in name:
                    continue

                # Get the name and value
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


# Filter/sorting
def backend_table(data, filter_query, sort_by, page_current):
    # Sort the data if it's defined (single column only)
    if len(sort_by):
        data.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=True
        )

    # Filter the data if it's defined
    filtering_expressions = filter_query.split(' && ')
    for filter_part in filtering_expressions:
        # Get the filter properties
        col_name, operator, filter_value = split_filter_part(filter_part)

        # Apply the filter
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            data = data.loc[getattr(data[col_name], operator)(filter_value)]
        elif operator == 'contains':
            data = data.loc[data[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            data = data.loc[data[col_name].str.startswith(filter_value)]

    # Get the page data
    page_size = TABLE_PAGE_SIZE
    page_count =int(len(data.index)/TABLE_PAGE_SIZE)

    # Get the column names in the right format
    columns = [{"name": i, "id": i} for i in data.columns]

    # Get the data to display in the table
    data = data.iloc[page_current*TABLE_PAGE_SIZE:(page_current+ 1)*TABLE_PAGE_SIZE].to_dict('records')

    return data, page_size, page_count, columns

# Filter the data for plotting
def filter_data(data, filter_query, sort_by, selected_rows):
    # Process inputs
    if selected_rows is None:
        selected_rows = []
    if filter_query is None:
        filter_query = ''
    if sort_by is None:
        sort_by = []

    # Sort the data if it's defined (single column only)
    if len(sort_by):
        data.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=True
        )

    # Filter the data if it's defined
    filtering_expressions = filter_query.split(' && ')
    for filter_part in filtering_expressions:
        # Get the filter properties
        col_name, operator, filter_value = split_filter_part(filter_part)

        # Apply the filter
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            data = data.loc[getattr(data[col_name], operator)(filter_value)]
        elif operator == 'contains':
            data = data.loc[data[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            data = data.loc[data[col_name].str.startswith(filter_value)]

    # Only plot selected points if some are selected
    if selected_rows is None or not selected_rows:
        plot_data = data
    else:
        plot_data = data.iloc[selected_rows]

    return plot_data

##==================================
## Datatable functions
##==================================
# Data table styling
def data_table_style():
    css = [dict(selector = '.row', rule = 'margin: 0')]
    style_table = dict(overflowX = 'scroll')
    style_cell = dict(padding= '5px', fontFamily= 'arial', fontSize = 14)
    return css, style_table, style_cell

# Take a dataframe and make it into a table
def df_to_table(id,df,selected_rows,filter_query,sort_by):
    # Change to empty list if "None"
    if selected_rows is None:
        selected_rows = []
    if filter_query is None:
        filter_query = ''
    if sort_by is None:
        sort_by = []

    # Make columns unique for data table
    df_new = unique_columns(df)

    # Get table styling
    css, style_table, style_cell = data_table_style()

    # Make table
    table_out = dt.DataTable(
        id             = id,
        data           = df_new.to_dict('records'),
        columns        = [{"name": i, "id": i} for i in df_new.columns],

        page_current   = 0,
        page_size      = TABLE_PAGE_SIZE,

        sort_action    = 'native',
        filter_action  = 'native',
        row_selectable = "multi",
        filter_query   = filter_query,
        sort_by        = sort_by,

        editable       = True,
        row_deletable  = False,
        selected_rows  = selected_rows,

        css            = css,
        style_table    = style_table,
        style_cell     = style_cell,
    )
    return table_out

# Create an empty table with a given ID
def empty_table(id):
    table_out = dt.DataTable(
        id = id,
        data = [{}],
    )
    return table_out
