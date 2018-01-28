from cement.core.controller import CementBaseController, expose

from pvmanager.manager.file import FileManager

class MediaManager(CementBaseController):
  class Meta:
    label = "media"
    stacked_on = "base"
    stacked_type = "nested"
    description = "Media manager."

  def __init__(self, basePath="."):
    CementBaseController.__init__(self)
    self.file_manager = FileManager(basePath)

  @expose(help="List available installation media.")
  def list(self):
    self.app.render(dict(data=self.file_manager.list()), "list.m")
