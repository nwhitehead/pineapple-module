
import pip
from pip.utils import get_installed_distributions

def freeze():
    '''
    Show arguments to require() to recreate what has been installed
    '''
    installations = {}
    for dist in get_installed_distributions():
        req = pip.FrozenRequirement.from_dist(dist, [], find_tags=False)
        installations[req.name] = req

    return [str(installation).rstrip() for installation in
        sorted(installations.values(), key=lambda x: x.name.lower())]

def require(*args, **kwargs):
    '''
    Install a set of packages using pip
    
    This is designed to be an interface for IPython notebooks that
    replicates the requirements.txt pip format. This lets notebooks
    specify which versions of packages they need inside the notebook
    itself.

    This function is the general-purpose interface that lets
    the caller specify any version string for any package.

    '''
    # If called with no arguments, returns requirements list
    if not args and not kwargs:
        return freeze()

    # Construct array of requirements
    requirements = list(args)
    extra = ['{}{}'.format(kw, kwargs[kw]) for kw in kwargs]
    requirements.extend(extra)
    args = ['install', '-q']
    args.extend(requirements)
    pip.main(args)

