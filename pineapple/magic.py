from .require import require as mod_require
import pip as mod_pip

from IPython.core.magic import (
    register_line_magic, register_cell_magic,
    register_line_cell_magic)

@register_line_magic
def require(line):
    if line == '':
        return ' '.join(mod_require())
    args = line.split(' ')
    mod_require(*args)

@register_line_magic
def pip(line):
    mod_pip.main(line.split(' '))

# Delete functions so that automagic can work properly
del pip, require
