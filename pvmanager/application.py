"""
The module handling around the main application objects.
"""

from pathlib import Path
import re

from cement.core.foundation import CementApp
from cement.utils.misc import init_defaults

from pvmanager.base_controller import BaseController
from pvmanager.manager.config import ConfigManager
from pvmanager.manager.media import MediaManager
from pvmanager.manager.media.firmware import FirmwareMediaManager
from pvmanager.manager.media.image import ImageMediaManager
from pvmanager.manager.media.install import InstallMediaManager
from pvmanager.manager.vm import VmManager


# define our default configuration options
DEFAULTS = init_defaults("pvmanager")
DEFAULTS["pvmanager"]["debug"] = False
DEFAULTS["pvmanager"]["prefix"] = "{}/.pvmanager".format(Path.home())


# define any hook functions here
def convert_general_to_snake(general_name):
  """Convertion of general strings to snake case."""

  no_spaces = re.sub(r'[\t \-*+]', '_', general_name)
  no_camel_case = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', no_spaces)
  extended_snake_case = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', no_camel_case).lower()
  snake_case = re.sub(r'_+', '_', extended_snake_case)

  return re.sub(r'^_|_$', '', snake_case)


def process_extra_arguments(app):
  """Converting extra arguments to safe snake case strings."""

  size = len(app.pargs.extra_arguments)
  if 0 < size:
    app.pargs.extra_arguments[0] = convert_general_to_snake(app.pargs.extra_arguments[0])


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
      ('post_argument_parsing', process_extra_arguments)
    ]
    extensions = ["mustache"]
    output_handler = "mustache"
    base_controller = "base"
    handlers = [BaseController, ConfigManager, MediaManager, FirmwareMediaManager, ImageMediaManager, InstallMediaManager, VmManager]
    template_module = "pvmanager.templates"
    arguments_override_config = True


def main():
  """The application main point."""
  with PVManagerApp() as app:
    app.args.add_argument('--prefix', action='store', dest='prefix')
    app.run()


if __name__ == '__main__':
  main()
