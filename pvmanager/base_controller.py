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
The BaseController and the application root logic.
"""

from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController


class JustAClass:
  @expose(help="Some info...")
  def command2(self):
    print("nothing interesting...")


class BaseController(AbstractBaseController, JustAClass):
  """
  The application root controller.
  """
  class Meta:
    """
    The meta configuration of the BaseController.
    """
    label = "base"
    description = "Python VM manager."

  def _setup(self, app_obj):
    """The base controller setup."""
    super(BaseController, self)._setup(app_obj)

    if not self.home_path.exists():
      app_obj.log.info("creating app home ({})".format(self.home_path))
      self.home_path.mkdir()

  @expose(help="this command does relatively nothing useful")
  def command1(self):
    self.app.log.info("Inside MyBaseController.command1()")
