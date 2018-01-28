from cement.core.controller import CementBaseController, expose


class AbstractBaseController(CementBaseController):
  """
  This is an abstract base class that is useless on its own, but used
  by other classes to sub-class from and to share common commands and
  arguments.  This should not be confused with the actual base
  controller.

  """
  class Meta:
    stacked_on = "base"
    stacked_type = "nested"

  def _setup(self, base_app):
    super(AbstractBaseController, self)._setup(base_app)

    # add a common object that will be used in any sub-class
    # pylint: disable=W0201
    self.reusable_dict = dict()
