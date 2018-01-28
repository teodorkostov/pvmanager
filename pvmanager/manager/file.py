from pathlib import Path


class FileManager:
  def __init__(self, base_path):
    self._path = Path(base_path)

  def list(self):
    return self._path.iterdir()
