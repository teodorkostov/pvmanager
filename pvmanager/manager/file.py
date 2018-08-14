# Copyright (C) 2018 Teodor Kostov
#
# This file is part of Python VM Manager.
#
# Python VM Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Python VM Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Python VM Manager.  If not, see <http://www.gnu.org/licenses/>.

"""
The FileManager and raw file handling operations.
"""

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
