from cement.core.controller import CementBaseController, expose
from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults

from media_manager import MediaManager

# define our default configuration options
defaults = init_defaults("myapp")
defaults["myapp"]["debug"] = False

# define any hook functions here
def cleanup_hook(app):
  pass

class JustAClass:
  @expose(help = "Some info...")
  def command2(self):
    print("nothing interesting...")

class MyBaseController(CementBaseController, JustAClass):
  class Meta:
    label = "base"
    description = "My Application does amazing things!"

  def __init__(self):
    CementBaseController.__init__(self)
    self.wtf = "come on..."

  @expose(hide=True)
  def default(self):
    self.app.log.info(">>>>>>>>>>>>> Inside MyBaseController.default()")
    data = [{'name': "1"}, {'name': "2"}, {'name': "asdf"}, {'name': "asdf"}]
    self.app.render(dict(data=data), "list.m")
    print(self.wtf)
    # always return the data, some output handlers require this
    # such as Json/Yaml (which don't use templates)
    return data

  @expose(help="this command does relatively nothing useful")
  def command1(self):
    self.app.log.info("Inside MyBaseController.command1()")

# define the application class
class PVManagerApp(CementApp):
  class Meta:
    label = "pvmanager"
    config_defaults = defaults
    hooks = [
      ('pre_close', cleanup_hook),
    ]
    extensions = ["mustache"]
    output_handler = "mustache"
    base_controller = "base"
    handlers = [MyBaseController, MediaManager]
    template_module = "templates"

with PVManagerApp() as app:
  app.run()
