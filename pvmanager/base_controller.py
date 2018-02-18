from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController


class JustAClass:
  @expose(help="Some info...")
  def command2(self):
    print("nothing interesting...")


class BaseController(AbstractBaseController, JustAClass):
  class Meta:
    label = "base"
    description = "Python VM manager."

  def _setup(self, app_obj):
    """The base controller setup."""
    super(BaseController, self)._setup(app_obj)

    if not self.home_path.exists():
      app_obj.log.info("creating app home ({})".format(self.home_path))
      self.home_path.mkdir()

  @expose(hide=True)
  def default(self):
    self.app.args.print_help()

  @expose(help="this command does relatively nothing useful")
  def command1(self):
    self.app.log.info("Inside MyBaseController.command1()")
