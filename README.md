# Wiz
Wiz is a web-based app for interactive data visualisation. As part of our original publication, we host a version of Wiz available at anytime at https://wiz.shef.ac.uk/. This repository contains all of the structure needed for users to create their own web apps.

## Contributing
We welcome any suggestions or contributions from the community. If we see enough value in community contributions, we will add them here or to the Wiz app as well.

## Basic Usage
To run an individual instance on a local machine, ensure that you have installed the necessary python packages,

`pip3 install -r requirements.txt`

Then simply run the executable `index.py`.

`python3 index.py`

By default, the app will then be hosted locally at port 5115. For example, that means that once the command window is running the code, then go to http://127.0.0.1:5115 to see the result.

## Folder Descriptions

### datasets
Datasets that can be used with Wiz or that can be used to develop your own app.

### src
All of the necessary source code for Wiz. The documentation for the structure of the Wiz code is shown below.

## Source Code File Organization
Wiz is built modularly. That means that each page has its own folders for layout and a file for callbacks. Going through the folder ...

```
src/
     assets/
     callbacks/
     functions/
     layouts/

    app.py
    index.py
    requirements.txt
```

### `assets`
This folder holds all of the external files (styling, etc.) for the app. Dash automatically looks for this folder on the initial load. The only time you have to reference any of the content in here is if you are uploading an image or video.

### `callbacks`
This folder has all of the callbacks. Every callback file is imported in the ``index.py`` function. Notice that the names of components in the callbacks correspond to the file/page name that they serve.

### `functions`
Many of the callbacks require lengthy calculations. All of those have been moved to this folder. Each page has its own set of functions. Where possible, commonly used functions are defined separately for conveinience.

### `layouts`
This folder holds all of the layouts. There is a high-level file for each layout that is intuitive to read. For example, the home page ``layouts/lines.py``. It imports the layout features from the other layout folders then assembles the layout to send back to ``index.py``.


```python
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
```

### ``app.py``
This is the app instance that is actually being seen in the browser.

#### ``index.py``
Entry point and the gatekeeper for all callbacks/layouts.

#### ``requirements.txt``
Python package requirements used to initialize the app.
