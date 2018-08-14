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
This FirmwareMediaManager all relevant functionality.
"""


from pvmanager.generic_media_controller import GenericMediaController



class FirmwareMediaManager(GenericMediaController):
  """The Firmware Media Manager handles the firmware media in $prefix/media/firmware/."""


  class Meta:
    """The Firmware Media Manager meta configuration."""
    label = 'firmware'
    description = """
    Firmware Media Manager handles the firmware media resources.
    All files are located at $prefix/media/firmware/.
    """
