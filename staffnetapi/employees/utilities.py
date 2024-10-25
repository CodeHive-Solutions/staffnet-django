# This file contains utility functions that are used in the employees app.
def capitalize_name(name: str) -> str:
    return name.title()


def user_photo_path(instance, _):
    return f"employees/photos/{instance.identification}.webp"
