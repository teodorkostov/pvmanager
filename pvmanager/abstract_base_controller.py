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
The AbstractBaseController and core controller functionality.
"""

from pathlib import Path

from cement.core.controller import CementBaseController
from cement.core.controller import expose


class AbstractBaseController(CementBaseController):
  """
  This is an abstract base class that is useless on its own, but used
  by other classes to sub-class from and to share common commands and
  arguments.  This should not be confused with the actual base
  controller.
  """


  class Meta:
    """The meta configuration options for all controllers."""
    stacked_on = 'base'
    stacked_type = 'nested'
    config_section = 'pvmanager'


  def __init__(self):
    CementBaseController.__init__(self)
    self.app_name = 'pvmanager'
    self.home_path = Path.home() / '.{}'.format(self.app_name)


  def _setup(self, app_obj):
    """The default cement controller setup."""
    super(AbstractBaseController, self)._setup(app_obj)

    # add a common object that will be used in any sub-class
    # pylint: disable=W0201
    self.reusable_dict = dict()


  def get_config(self, key):
    """Helper method to get config properties for the current application."""
    return self.app.config.get(self.app_name, str(key))


  @expose(hide=True)
  def default(self):
    """Default command handler just prints out the help information."""
    self.app.args.print_help()
