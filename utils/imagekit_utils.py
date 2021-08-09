from werkzeug.datastructures import FileStorage
from app import imagekit


def upload_image(image: FileStorage):
    return imagekit.upload_file(
        file=image,
        file_name=image.filename,
        options={
            "folder": "/inventory",
            "is_private_file": False,
            "use_unique_file_name": True,
        },
    )

def delete_image(image_id: str):
    return imagekit.delete_file(image_id)
