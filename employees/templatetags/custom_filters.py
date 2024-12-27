from django import template

register = template.Library()

@register.filter
def display_value(field):
    """
    Returns the string representation of the field's value.
    If it's a ForeignKey, fetch the related object.
    """
    if hasattr(field, "field") and hasattr(field.field, "queryset"):
        queryset = field.field.queryset
        if queryset and field.value:
            return queryset.get(pk=field.value)  # Get the related object
    return field.value if field.value else "N/A"
