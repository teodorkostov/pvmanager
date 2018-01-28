from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController
from pvmanager.manager.file import FileManager


class MediaManager(AbstractBaseController):
  """The Media Manager handles the creation and removal of VM installations."""
  class Meta:
    """The Media Manager meta configuration."""
    label = "media"
    description = "Media manager that handles the different VM installations."

  def __init__(self):
    AbstractBaseController.__init__(self)

  @expose(hide=True)
  def default(self):
    """Default command handler just prints out the help information."""
    self.app.args.print_help()

  @expose(help="List available installation media.")
  def list(self):
    """The `list` command prints out all of the VM installations in the chosen root path."""
    base_path = self.app.config.get('myapp', 'prefix')
    file_manager = FileManager(base_path)
    self.app.render(dict(data=file_manager.list()), "list.m")
