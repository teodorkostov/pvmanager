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
The MediaManager and all media handling functionality.
"""

from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController
from pvmanager.manager.file import FileManager


class MediaManager(AbstractBaseController):
  """The Media Manager handles the creation and removal of VM installations."""
  class Meta:
    """The Media Manager meta configuration."""
    label = "media"
    description = """
    Media manager that handles the different VM installations.
    """

  def __init__(self):
    AbstractBaseController.__init__(self)

  @expose(help="List available installation media.")
  def list(self):
    """The `list` command prints out all of the VM installations in the chosen root path."""
    base_path = self.get_config("prefix")
    file_manager = FileManager(self)
    self.app.render(dict(data=file_manager.list()), "list.m")
