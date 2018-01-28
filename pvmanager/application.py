from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults

from pvmanager.base_controller import BaseController
from pvmanager.manager.media import MediaManager


# define our default configuration options
DEFAULTS = init_defaults("pvmanager")
DEFAULTS["pvmanager"]["debug"] = False
DEFAULTS["pvmanager"]["prefix"] = "."


# define any hook functions here
def cleanup_hook(app):
  pass


class PVManagerApp(CementApp):
  """The main application class.

  The main application extends CementApp in order to become a CLI.
  """
  class Meta:
    """The meta configuration for the main application.

    Attributes:
      label (string)              : The name of the application.
      config_defaults (dictionary): The standard cement configuration options.
      hooks (array)               : Application lifecycle functionality.
      extensions (array)          : Additional plugins.
      base_controller (string)    : The name of the base app controller.
      handlers (array)            : All application controllers.
      template_module (string)    : The name of the module with mustache templates.
    """
    label = "pvmanager"
    config_defaults = DEFAULTS
    hooks = [
      ('pre_close', cleanup_hook),
    ]
    extensions = ["mustache"]
    output_handler = "mustache"
    base_controller = "base"
    handlers = [BaseController, MediaManager]
    template_module = "pvmanager.templates"
    arguments_override_config = True


def main():
  """The application main point."""
  with PVManagerApp() as app:
    app.args.add_argument('--prefix', action='store', dest='prefix')
    app.run()


if __name__ == '__main__':
    main()
