from pathlib import Path


class FileManager:
  def __init__(self, parent):
    self._parent = parent
    self._path = Path(parent.get_config("prefix"))

  def exists(self):
    return self._path.exists()

  def list(self):
    if not self.exists():
      self._parent.app.log.error("prefix ({}) is not initialized".format(self._path))
      return []
    return self._path.iterdir()
