import io

from PIL import Image


def get_image_from_bytes(binary_image, max_size=1024):
    # input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    input_image = Image.open(io.BytesIO(binary_image.file.read()))
    width, height = input_image.size
    resize_factor = min(max_size / width, max_size / height)
    resized_image = input_image.resize(
        (
            int(input_image.width * resize_factor),
            int(input_image.height * resize_factor),
        )
    )
    return resized_image, resized_image.width, resized_image.height
