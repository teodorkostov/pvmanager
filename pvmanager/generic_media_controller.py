"""
The GenericMediaController and reusable media functionality.
"""

from pathlib import Path

from pvmanager.abstract_base_controller import AbstractBaseController



class GenericMediaController(AbstractBaseController):
  """
  This is an base class for common media operations.
  """


  class Meta:
    """The meta configuration options for this controllers."""
    stacked_on = 'media'
    arguments = [
      (['extra_arguments'], dict(action='store', nargs='*'))
    ]


  def __init__(self):
    AbstractBaseController.__init__(self)
    self.media_path = None


  def _setup(self, app_obj):
    """The default cement controller setup."""
    super(GenericMediaController, self)._setup(app_obj)

    self.media_path = Path(self.get_config('prefix')) / 'media' / self.Meta.label
    if not self.media_path.exists():
      app_obj.log.info('creating {} media path ({})'.format(self.Meta.label, self.media_path))
      self.media_path.mkdir(parents=True)


  def _render(self, result):
    print('  {}'.format(result))
