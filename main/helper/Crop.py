from PIL import Image

from django.core.files.base import ContentFile

def cropper(original_image, area):
    img_io = StringIO.StringIO()
    cropped_img = original_image.crop(area)
    cropped_img.save(img_io, format='JPEG', quality=100)
    img_content = ContentFile(img_io.getvalue(), 'temp.jpg')
    return img_content