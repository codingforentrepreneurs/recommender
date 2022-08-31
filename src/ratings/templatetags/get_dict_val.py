from django.template.defaulttags import register

@register.filter
def get_dict_val(dictionary, key, key_as_str=True):
    if not isinstance(dictionary, dict):
        return None
    if key_as_str:
        key = f"{key}"
    return dictionary.get(key)
