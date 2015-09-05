
from .require import *
from .runtest import *

# Only use magic in IPython
try:
    get_ipython()
    from .magic import *
except NameError:
    pass
