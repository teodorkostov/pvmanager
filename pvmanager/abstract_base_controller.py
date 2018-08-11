"""
The AbstractBaseController and core controller functionality.
"""

from pathlib import Path

from cement.core.controller import CementBaseController
from cement.core.controller import expose


class AbstractBaseController(CementBaseController):
  """
  This is an abstract base class that is useless on its own, but used
  by other classes to sub-class from and to share common commands and
  arguments.  This should not be confused with the actual base
  controller.
  """


  class Meta:
    """The meta configuration options for all controllers."""
    stacked_on = 'base'
    stacked_type = 'nested'
    config_section = 'pvmanager'


  def __init__(self):
    CementBaseController.__init__(self)
    self.app_name = 'pvmanager'
    self.home_path = Path.home() / '.{}'.format(self.app_name)


  def _setup(self, app_obj):
    """The default cement controller setup."""
    super(AbstractBaseController, self)._setup(app_obj)

    # add a common object that will be used in any sub-class
    # pylint: disable=W0201
    self.reusable_dict = dict()


  def get_config(self, key):
    """Helper method to get config properties for the current application."""
    return self.app.config.get(self.app_name, str(key))


  @expose(hide=True)
  def default(self):
    """Default command handler just prints out the help information."""
    self.app.args.print_help()
