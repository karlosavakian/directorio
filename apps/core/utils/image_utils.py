from PIL import Image, ImageOps


def resize_image(image_path, max_size=(800, 800)):
    """Resize the image at ``image_path`` keeping aspect ratio."""
    img = Image.open(image_path)
    img = ImageOps.exif_transpose(img)
    img.thumbnail(max_size, Image.LANCZOS)
    img.save(image_path, format=img.format)

