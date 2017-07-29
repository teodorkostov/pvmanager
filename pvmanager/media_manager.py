from cement.core.controller import CementBaseController, expose

from file_manager import FileManager

class MediaManager(CementBaseController):
  class Meta:
    label = "media"
    stacked_on = "base"
    stacked_type = "nested"
    description = "Media manager."

  def __init__(self, basePath = "."):
    CementBaseController.__init__(self)
    # self.fileManager = FileManager(basePath + "/media")
    self.fileManager = FileManager(basePath)

  @expose(help = "List available installation media.")
  def list(self):
    self.app.render(dict(data=self.fileManager.list()), "list.m")
