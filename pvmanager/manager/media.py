from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController
from pvmanager.manager.file import FileManager


class MediaManager(AbstractBaseController):
  class Meta:
    label = "media"
    description = "Media manager that handles the different VM installations."

  def __init__(self):
    AbstractBaseController.__init__(self)

  @expose(hide=True)
  def default(self):
    self.app.args.print_help()

  @expose(help="List available installation media.")
  def list(self):
    base_path = self.app.config.get('myapp', 'prefix')
    file_manager = FileManager(base_path)
    self.app.render(dict(data=file_manager.list()), "list.m")
