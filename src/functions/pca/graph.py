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
from functions.pca.data import *

##==================================
## General functions
##==================================
def graph_configure(value):
    return dict(
        displayModeBar = value,
        showSendToCloud = False,
        toImageButtonOptions = dict(
            format = 'svg',
        ),
        displaylogo = False,
        watermark = False,
        responsive = True,
        editable = True,
        edits = dict(
            titleText = False,
        )
    )

def PCA_plot(Y, df, var_exp, cum_var_exp, class_select, click_data):
    if len(list(Y)) > 1:
        out_figure = dict(
              data = PCA_1(Y, df, class_select),
              layout = PCA_1_layout(Y, click_data)
            )

        animate = False
        out_style = dict(height = '100%', width = '50%', display = 'inline-block')
    else:
        out_figure = dict(
            data = [],
            layout = blank_layout()
        )
        out_style = dict(height = '100%', width = '50%', display = 'inline-block')
        animate = False

    return out_style, out_figure, animate

def LDA_plot(Y, df, var_exp, cum_var_exp, class_select):
    if len(list(Y)) > 1:
        out_figure =  dict(
              data   = LDA_1(Y, df, class_select),
              layout = LDA_1_layout(Y)
            )

        animate = False
        out_style = dict(height = '100%', width = '50%', display = 'inline-block')
    else:
        out_figure = dict(
            data = [],
            layout = blank_layout()
        )
        out_style = dict(height = '100%', width = '50%', display = 'inline-block')
        animate = False

    return out_style, out_figure, animate

def PCA_plot_2(var_exp, cum_var_exp):
    if len(var_exp) > 1:
        out_figure = dict(
              data = PCA_2(var_exp, cum_var_exp),
              layout = PCA_2_layout()
            )
        out_style = dict(height = '100%', width = '50%', display = 'inline-block')

    else:
        out_figure = dict(
            data = [],
            layout = blank_layout()
        )
        out_style = dict(height = '100%', width = '50%', display = 'inline-block')

    return out_style, out_figure

def LDA_plot_2(var_exp, cum_var_exp):
    if len(var_exp) > 1:
        out_figure = dict(
            data   = LDA_2(var_exp, cum_var_exp),
            layout = PCA_2_layout()
        )
        out_style = dict(height = '100%', width = '50%', display = 'inline-block')
    else:
        out_figure = dict(
            data = [],
            layout = blank_layout()
        )
        out_style = dict(height = '100%', width = '50%', display = 'inline-block')

    return out_style, out_figure
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
## Layout and data
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

def PCA_1_layout(Y, click_data):

    x_column =  ['PC 1', '']
    y_column = ['PC 2', '']
    x_type = 'linear'
    y_type = 'linear'

    # Set up annotations
    annotation = [];
    if click_data is not None:
        # Get the label and x/y info
        x_loc = click_data['points'][0]['x']
        y_loc = click_data['points'][0]['y']
        x_text = str(x_loc)
        y_text = str(y_loc)

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
            text        = x_column[0] + ': ' + x_text + '<br>' + y_column[0] + ': ' +
                y_text + '<br>'
            )
        annotation.append(annotation_text)

    return go.Layout(
            autosize    = True,
            title       = dict(text = ' '),
            xaxis       = axis_layout_2D(x_column, x_type),
            yaxis       = axis_layout_2D(y_column, y_type),
            annotations = annotation,
            font        =  dict(
                family = FONT_FAMILY['plot'],
                size   = FONT_SIZE['plot'],
            ),
            hovermode   = 'closest',
            margin      = dict(l = 50, b = 40, t = 10, r = 30),
            uirevision  ='foo',
            legend      = dict(x = 1.02, y = 0.98),
            template    = TEMPLATE
        )


def PCA_1(Y, df, class_select):
    if class_select is not None:
        # Initialize traces
        traces = []

        # Loop through all of the x-values
        for name in df[class_select].unique():
            # Add trace
            traces.append(
                go.Scatter(
                    x       = Y[df[class_select] == name,0],
                    y       = Y[df[class_select] == name,1],
                    mode    = 'markers',
                    name    = name,
                    opacity = OPACITY,
                    marker  = dict(
                        size       = 15,
                        sizemode   = 'diameter',
                        colorscale = COLORSCALE,
                        line       = dict(
                            width = 0.5,
                            color = 'white'
                        ),
                    )
                )
            )
    else:
        traces = [go.Scatter(
            x       = Y[:,0],
            y       = Y[:,1],
            mode    = 'markers',
            opacity = OPACITY,
            marker  = dict(
                size       = 15,
                sizemode   = 'diameter',
                colorscale = COLORSCALE,
                line       = dict(
                    width = 0.5,
                    color = 'white'
                ),
            )
        )]

    return traces

def PCA_2_layout():

    x_column =  ['', '']
    y_column = ['Variance (%)', '']
    x_type = 'linear'
    y_type = 'linear'

    return go.Layout(
            autosize   = True,
            title      = dict(text = ' '),
            xaxis      = axis_layout_2D(x_column, x_type),
            yaxis      = axis_layout_2D(y_column, y_type),
            font       =  dict(
                family = FONT_FAMILY['plot'],
                size   = FONT_SIZE['plot'],
            ),
            hovermode  = 'closest',
            margin     = dict(l = 50, b = 40, t = 10, r = 30),
            uirevision ='foo',
            legend     = dict(x = 1.02, y = 0.98),
            template   = TEMPLATE
        )


def PCA_2(var_exp, cum_var_exp):
    n = len(var_exp)

    trace1 = dict(
        type = 'bar',
        x    = ['PC %s' %i for i in range(1,n+1)],
        y    = var_exp,
        name = 'Individual'
    )

    trace2 = dict(
        type = 'scatter',
        x    = ['PC %s' %i for i in range(1,n+1)],
        y    = cum_var_exp,
        name = 'Cumulative'
    )

    traces = [trace1, trace2]

    return traces

def LDA_1_layout(Y):

    x_column =  ['LD 1', '']
    y_column = ['LD 2', '']
    x_type = 'linear'
    y_type = 'linear'

    return go.Layout(
            autosize   = True,
            title      = dict(text = ' '),
            xaxis      = axis_layout_2D(x_column, x_type),
            yaxis      = axis_layout_2D(y_column, y_type),
            font       =  dict(
                family = FONT_FAMILY['plot'],
                size   = FONT_SIZE['plot'],
            ),
            hovermode  = 'closest',
            margin     = dict(l = 50, b = 40, t = 10, r = 30),
            uirevision ='foo',
            legend     = dict(x = 1.02, y = 0.98),
            template   = TEMPLATE,
        )

def LDA_1(Y, df, class_select):
    # Initialize traces
    traces = []

    # Loop through all of the x-values
    for name in df[class_select].unique():
        # Add trace
        traces.append(
            go.Scatter(
                x       = Y[df[class_select] == name,0]*-1,  # Flipped!
                y       = Y[df[class_select] == name,1]*-1,
                mode    = 'markers',
                name    = name,
                opacity = OPACITY,
                marker  = dict(
                    size       = 15,
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

def LDA_2(var_exp, cum_var_exp):
    n = len(var_exp)
    x = ['LD %s' %i for i in range(1,n+1)]

    trace1 = dict(
        type = 'bar',
        x    = x,
        y    = var_exp,
        name ='Individual'
    )

    trace2 = dict(
        type = 'scatter',
        x    = x,
        y    = cum_var_exp,
        name = 'Cumulative'
    )

    traces = [trace1, trace2]

    return traces
# If it is run as the main function
if __name__ == '__main__':
    print('')
