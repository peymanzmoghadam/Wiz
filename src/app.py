import dash
from flask_caching import Cache

##==================================
## Initialize app
##==================================
# Establish application
app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True

# Title (in tab)
app.title = 'Wiz'

##==================================
## Caching
##==================================
CACHE_DIRECTORY = '._cache-directory'
cache = Cache(app.server,
    config = {
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': CACHE_DIRECTORY,
        'CACHE_THRESHOLD': 1000,
        'CACHE_DEFAULT_TIMEOUT': 3000
    }
)
