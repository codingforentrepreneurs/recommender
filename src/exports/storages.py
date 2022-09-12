from django.core.files.storage import default_storage


def save(fpath, file_obj, overwrite=False):
    """
    Export a file directly to your default
    django storage with the option to 
    overwrite the curernt item
    """
    if overwrite is True and default_storage.exists(fpath):
        default_storage.delete(fpath)
    default_storage.save(fpath, file_obj)