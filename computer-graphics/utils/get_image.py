import os


def get_image_path(name):
    current_directory = os.path.dirname(__file__)
    image_path = os.path.join(current_directory, "..", "assets", name)
    return image_path
