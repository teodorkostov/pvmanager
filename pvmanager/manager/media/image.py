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
This ImageMediaManager all relevant functionality.
"""

import subprocess

from cement.core.controller import expose

from pvmanager.generic_media_controller import GenericMediaController



USAGE = 'usage: ... image create <VM name> <size>'

class ImageMediaManager(GenericMediaController):
  """The Image Media Manager handles the VM media in $prefix/media/image/."""


  class Meta:
    """The Image Media Manager meta configuration."""
    label = 'image'
    description = """
    Image Media Manager handles the VM media resources (images).
    All files are located at $prefix/media/image/.
    """


  def _get_file_path(self, file_name):
    file_path = super(ImageMediaManager, self)._get_file_path(file_name)
    return file_path.with_suffix('.raw')


  @expose(help="""
    Create a new VM image.
    {}
  """.strip().format(USAGE))
  def create(self):
    """Handler for the image creation."""
    size = len(self.app.pargs.extra_arguments)
    if 2 > size:
      self.app.log.error(USAGE)
      return

    vm_name = self.app.pargs.extra_arguments[0].safe_value
    vm_image_path = self._get_file_path(vm_name)
    vm_image_size = self.app.pargs.extra_arguments[1].original_value

    if vm_image_path.exists():
      self.app.log.error(
          'a VM image with the same name ({}) already exists'.format(vm_image_path.stem))
      return

    subprocess_arguments = ['qemu-img', 'create', '-f', 'raw', vm_image_path, vm_image_size]

    subprocess.call(subprocess_arguments)
