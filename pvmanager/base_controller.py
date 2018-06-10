"""
The BaseController and the application root logic.
"""

from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController


class JustAClass:
  @expose(help="Some info...")
  def command2(self):
    print("nothing interesting...")


class BaseController(AbstractBaseController, JustAClass):
  """
  The application root controller.
  """
  class Meta:
    """
    The meta configuration of the BaseController.
    """
    label = "base"
    description = "Python VM manager."

  def _setup(self, app_obj):
    """The base controller setup."""
    super(BaseController, self)._setup(app_obj)

    if not self.home_path.exists():
      app_obj.log.info("creating app home ({})".format(self.home_path))
      self.home_path.mkdir()

  @expose(help="this command does relatively nothing useful")
  def command1(self):
    self.app.log.info("Inside MyBaseController.command1()")
