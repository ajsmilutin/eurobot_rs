from wagtail.images.formats import Format, register_image_format, unregister_image_format
from django.utils.translation import gettext_lazy as _

register_image_format(Format('original', _('Original'), 'img-responsive center-block', 'original'))
register_image_format(Format('thumbnail', _('Thumbnail'), 'richtext-image thumbnail', 'max-120x120'))