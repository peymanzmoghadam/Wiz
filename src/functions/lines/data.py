##==================================
## External imports
##==================================
import pandas as pd

##==================================
## Internal imports
##==================================
from functions.global_functions import *

##==================================
## Functions
##==================================
def get_labels(dframe, dataType):
    # Initialzie the labels
    x_labels = []
    y_labels = []
    size_labels = []

    if dataType == 1:
        x_labels = list(dframe)[0]
        for n in list(dframe)[1:]:
            y_labels.append(n)
            if dframe[n].dtype != 'object':
                size_labels.append(n)
    else:
        count = 0;
        for n in list(dframe)[0:]:
            if count == 1:
                y_labels.append(n)

                if dframe[n].dtype != 'object':
                    size_labels.append(n)
                count = 0
            else:
                x_labels.append(n)
                count = 1

    return x_labels, y_labels, size_labels

# Clean the data for plotting
def get_plot_data(df, y_column, datatype):
    # Column indicies
    cols = []
    if datatype == 1:
        cols.append(0)
        for n in y_column:
            cols.append(df.columns.get_loc(n))
    else:
        for n in y_column:
            temp = df.columns.get_loc(n)
            cols.append(temp-1)
            cols.append(temp)

    # Reduce data to what needs to be plotted or displayed in the table
    if y_column is not None or y_column != []:
        df_new = df[df.columns[cols]]
    else:
        df_new = df[[df.columns[0]]]

    return df_new

# If it is run as the main function
if __name__ == '__main__':
    print('')
