# This file contains utility functions that are used in the employees app.
def user_photo_path(instance, _):
    return f"employees/photos/{instance.identification}.webp"


def get_choices_values(choices):
    """Returns the value of a choice."""
    return [choice[0] for choice in choices]
