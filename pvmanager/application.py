from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults

# define our default configuration options
defaults = init_defaults('myapp')
defaults['myapp']['debug'] = False

# define any hook functions here
def cleanup_hook(app):
  pass

# define the application class
class PVManagerApp(CementApp):
  class Meta:
    label = 'pvmanager'
    config_defaults = defaults
    hooks = [
      ('pre_close', cleanup_hook),
    ]
