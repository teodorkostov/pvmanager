from pathlib import Path

class FileManager:
  def __init__(self, basePath = "."):
    self._path = Path(basePath)

  def list(self):
    return self._path.iterdir()
