from cement.core.controller import CementBaseController, expose


class AbstractBaseController(CementBaseController):
  """
  This is an abstract base class that is useless on its own, but used
  by other classes to sub-class from and to share common commands and
  arguments.  This should not be confused with the actual base
  controller.

  """
  class Meta:
    """The meta configuration options for all controllers."""
    stacked_on = "base"
    stacked_type = "nested"

  def __init__(self):
    CementBaseController.__init__(self)
    self.app_name = "pvmanager"

  def _setup(self, app_obj):
    """The default cement controller setup."""
    super(AbstractBaseController, self)._setup(app_obj)

    # add a common object that will be used in any sub-class
    # pylint: disable=W0201
    self.reusable_dict = dict()

  def get(self, key):
    """Helper method to get config properties for the current application."""
    self.app.config.get(self.app_name, key)
