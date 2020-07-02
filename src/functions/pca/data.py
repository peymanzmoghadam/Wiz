##==================================
## External imports
##==================================
import pandas as pd
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

##==================================
## Internal imports
##==================================
from functions.global_functions import *

##==================================
## Functions
##==================================
def get_labels(dframe):
    # Initialzie the labels
    class_labels = []

    # Class labels can only be categorical or a variable with less than 10 unique values
    for n in list(dframe):
        if 'object' == dframe[n].dtype:
            class_labels.append(n)
        elif len(dframe[n].unique()) < 10:
            class_labels.append(n)

    return class_labels

# Principle component analysis on data
def PCA(df, class_name):
    # Cannot do PCA on an empty matrix
    if len(list(df)) < 2:
        return df, [], [], []

    # Figure out which columns can be considered (only float or int columns but not the class column)
    cols = []
    for item in list(df):
        if 'float' in df[item].dtypes.name:
            if item != class_name:
                cols.append(df.columns.get_loc(item))

    # Get new dataframe
    df_new = df[df.columns[cols]]

    # Set this as the data to analyze
    X = df_new.values

    # Standardize the data
    X_std = StandardScaler().fit_transform(X)

    # Do PCA
    pca = sklearnPCA(n_components = len(list(df_new)))
    Y = pca.fit_transform(X_std)

    ## Get variance contributions
    var_exp = pca.explained_variance_ratio_
    cum_var_exp = pca.explained_variance_ratio_.cumsum()

    return Y, var_exp, cum_var_exp

def LDA(df, class_name):
    # Cannot do PCA on an empty matrix
    if len(list(df)) < 2:
        return df, [], [], []

    # Figure out which columns can be considered (only float or int columns but not the class column)
    cols = []
    for item in list(df):
        if 'float' in df[item].dtypes.name:
            if item != class_name:
                cols.append(df.columns.get_loc(item))

    # Get new dataframe
    df_new = df[df.columns[cols]]

    # Set this as the data to analyze
    X = df_new.values

    # LDA
    n = min(len(list(df_new)), len(df[class_name].unique()) - 1)
    lda = LinearDiscriminantAnalysis(n_components = n)
    Y_lda = lda.fit_transform(X, df[class_name])
    exp_var = lda.explained_variance_ratio_
    cum_var = lda.explained_variance_ratio_.cumsum()

    return Y_lda, exp_var, cum_var

# If it is run as the main function
if __name__ == '__main__':
    print('')
