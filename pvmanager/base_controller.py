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

  def __init__(self):
    AbstractBaseController.__init__(self)
    self.wtf = "come on..."

  @expose(hide=True)
  def default(self):
    self.app.args.print_help()

  @expose(help="this command does relatively nothing useful")
  def command1(self):
    self.app.log.info("Inside MyBaseController.command1()")
