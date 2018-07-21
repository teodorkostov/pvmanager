"""
This ImageMediaManager all relevant functionality.
"""


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
