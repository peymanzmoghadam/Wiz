##==================================
## External imports
##==================================
import os
import base64
import io
import uuid
from math import log10
from numpy import linspace, array
from numpy import append as ap
from itertools import compress
import pandas as pd
import json
import urllib
import plotly.graph_objs as go

##==================================
## Internal imports
##==================================
from functions.global_functions import *
from functions.lines.data import *

##==================================
## General functions
##==================================
def graph_configure(modeBar):
    if type(modeBar) is bool:
        editable = modeBar
    else:
        if 'hover' in modeBar:
            editable = True
        else:
            editable = False

    return dict(
        displayModeBar = modeBar,
        showSendToCloud = False,
        toImageButtonOptions = dict(
            format = 'svg',
        ),
        displaylogo = False,
        watermark = False,
        responsive = True,
        editable = editable,
        edits = dict(
            titleText = False,
        )
    )

def pick_plot(plot_data, columns, click_data, x_type, y_type, datatype):
    # If no data columns are selected
    if len(columns) <= 1:
        out_figure = dict(data = [], layout = blank_layout())
        out_style  = dict(height = '100%', width = '100%')
        animate    = False

    else:
        if datatype == 1:
            out_figure = dict(
              data   = lines_type1_data(plot_data),
              layout = lines_type1_layout(plot_data, x_type, y_type, click_data)
            )
        else:
            out_figure = dict(
              data = lines_type2_data(plot_data),
              layout = lines_type2_layout(plot_data, x_type, y_type, click_data)
            )

        animate = False
        out_style = dict(height = '100%', width = '100%')

    return out_style, out_figure, animate
##==================================
## Blank layout
##==================================
def blank_layout():
    return go.Layout(
        title = dict(text = ' '),
        xaxis = dict(
            autorange      = True,
            showgrid       = False,
            zeroline       = False,
            showline       = False,
            ticks          = '',
            showticklabels = False
        ),
        yaxis = dict(
            autorange      = True,
            showgrid       = False,
            zeroline       = False,
            showline       = False,
            ticks          = '',
            showticklabels =False
        )
    )
##==================================
## Lines
##==================================
def axis_layout_2D(column_info, type):

    axis_layout = dict(
        title      = '<b>' + column_info[0] + '<b>',
        showline   = True,
        linewidth  = AXIS_LINE_WIDTH,
        linecolor  = AXIS_LINE_COLOR,
        mirror     = True,
        ticks      = 'outside',
        showgrid   = False,
        zeroline   = False,
        autorange  = True,
        automargin = True,
        titlefont  = dict(
            family = FONT_FAMILY['plot_labels'],
            size   = FONT_SIZE['plot_labels'],
        )
    )

    if 'float' in column_info[1] or 'int' in column_info[1]:
        axis_layout.update(dict(type = type, nticks = 5))

    return axis_layout

def lines_type1_layout(df_clean, x_type, y_type, click_data):
    # Number of data columns
    n_var = len(list(df_clean)) - 1

    label_column = list(df_clean)[0]
    x_column =  [list(df_clean)[0], df_clean.dtypes[0].name]
    y_column = ['Y', df_clean.dtypes[1].name]

    # Create click annotation
    annotation = [];
    if click_data is not None:
        # Get the label and x/y info
        x_loc = click_data['points'][0]['x']
        y_loc = click_data['points'][0]['y']
        x_text = str(x_loc)
        y_text = str(y_loc)

        # Change label location if the axis is Log
        if x_type == 'log' and isinstance(x_loc, str) == 0:
            x_loc = log10(x_loc)
        if y_type == 'log' and isinstance(y_loc, str) == 0:
            y_loc = log10(y_loc)

        # Create annotation
        annotation_text = dict(
            x           = x_loc,
            y           = y_loc,
            align       = 'right',
            ax          = 180,
            ay          = 20,
            bgcolor     = '#666666',
            opacity     = OPACITY,
            font        = dict(color = 'white'),
            showarrow   = True,
            arrowhead   = 7,
            arrowsize   = 1,
            arrowwidth  = 2,
            clicktoshow = 'onout',
            text        = x_column[0] + ': ' + x_text + '<br>' + y_column[0]
                + ': ' + y_text + '<br>'
            )
        annotation.append(annotation_text)

    return go.Layout(
            autosize    = True,
            title       = dict(text = ' '),
            xaxis       = axis_layout_2D(x_column, x_type),
            yaxis       = axis_layout_2D(y_column, y_type),
            annotations = annotation,
            font        = dict(
                family = FONT_FAMILY['plot'],
                size   = FONT_SIZE['plot'],
            ),
            hovermode   = 'closest',
            margin      = dict(l = 50, b = 40, t = 10, r = 30),
            uirevision  = 'foo',
            legend      = dict(x=1.02, y=0.98),
            template    = TEMPLATE
        )

def lines_type2_layout(df_clean, x_type, y_type, click_data):
    # Number of data columns
    n_var = len(list(df_clean)) - 1

    label_column = list(df_clean)[0]
    x_column =  ['X', df_clean.dtypes[0].name]
    y_column = ['Y', df_clean.dtypes[1].name]

    # Create click annotation
    annotation = [];
    if click_data is not None:
        # Get the label and x/y info
        x_loc = click_data['points'][0]['x']
        y_loc = click_data['points'][0]['y']
        x_text = str(x_loc)
        y_text = str(y_loc)

        # Change label location if the axis is Log
        if x_type == 'log' and isinstance(x_loc, str) == 0:
            x_loc = log10(x_loc)
        if y_type == 'log' and isinstance(y_loc, str) == 0:
            y_loc = log10(y_loc)


        # Create annotation
        annotation_text = dict(
            x = x_loc,
            y = y_loc,
            align = 'right',
            ax = 180,
            ay = 20,
            bgcolor = '#666666',
            opacity = OPACITY,
            font = dict(color = 'white'),
            showarrow = True,
            arrowhead = 7,
            arrowsize = 1,
            arrowwidth = 2,
            clicktoshow = 'onout',
            text = x_column[0] + ': ' + x_text + '<br>' + y_column[0] + ': ' +
                y_text + '<br>'
            )
        annotation.append(annotation_text)

    return go.Layout(
            autosize    = True,
            title       = dict(text = ' '),
            xaxis       = axis_layout_2D(x_column, x_type),
            yaxis       = axis_layout_2D(y_column, y_type),
            annotations = annotation,
            font        = dict(
                family = FONT_FAMILY['plot'],
                size   = FONT_SIZE['plot'],
            ),
            hovermode   = 'closest',
            margin      = dict(l = 50, b = 40, t = 10, r = 30),
            uirevision  ='foo',
            legend      = dict(x=1.02, y=0.98),
            template    = TEMPLATE
        )

def lines_type1_data(df_clean):
    # Number of variables
    n_var = len(list(df_clean))

    # Initialize traces
    traces = []
    # Loop through all of the x-values
    for i in range(n_var):
        if i == 0:
            continue

        # Add categorical trace
        traces.append(
            go.Scatter(
                x         = df_clean.iloc[:,0],
                y         = df_clean.iloc[:,i],
                mode      = 'lines+markers',
                text      = list(df_clean)[i],
                name      = list(df_clean)[i],
                opacity   = OPACITY,
                hoverinfo = 'text',
                marker    = dict(
                    size       = 10,
                    sizemode   = 'diameter',
                    colorscale = COLORSCALE,
                    line       = dict(
                        width  = 0.5,
                        color  = 'white'
                    ),
                )
            )
        )

    return traces

def lines_type2_data(df_clean):
    # Number of variables
    n_var = len(list(df_clean))

    # Initialize traces
    traces = []
    # Loop through all of the x-values
    for i in range(0, n_var, 2):
        # Add categorical trace
        traces.append(
            go.Scatter(
                x         = df_clean.iloc[:,i],
                y         = df_clean.iloc[:,i+1],
                mode      = 'lines+markers',
                text      = list(df_clean)[i+1],
                name      = list(df_clean)[i+1],
                opacity   = OPACITY,
                hoverinfo = 'text',
                marker    = dict(
                    size       = 10,
                    sizemode   = 'diameter',
                    colorscale = COLORSCALE,
                    line       = dict(
                        width = 0.5,
                        color = 'white'
                    ),
                )
            )
        )

    return traces

# If it is run as the main function
if __name__ == '__main__':
    print('')
