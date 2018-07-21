"""
This ImageMediaManager all relevant functionality.
"""

from cement.core.controller import expose

from pvmanager.generic_media_controller import GenericMediaController



class ImageMediaManager(GenericMediaController):
  """The Image Media Manager handles the VM media in $prefix/media/image/."""


  class Meta:
    """The Image Media Manager meta configuration."""
    label = 'image'
    description = """
    Image Media Manager handles the VM media resources (images).
    All files are located at $prefix/media/image/.
    """


  def _get_image_path(self, general_vm_name):
    return self.media_path / '{}.raw'.format(general_vm_name)


  @expose(help='Create a new VM image in the current PREFIX.')
  def create(self):
    size = len(self.app.pargs.extra_arguments)
    if 1 > size:
      self.app.log.error('expected the VM name as an extra argument')
      return

    general_vm_name = self.app.pargs.extra_arguments[0]
    vm_instance_path = self._get_image_path(general_vm_name)

    if vm_instance_path.exists():
      self.app.log.error(
          'a VM with the same name ({}) already exists'.format(vm_instance_path.stem))
      return

    self._render(vm_instance_path)
