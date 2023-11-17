import sys

def add_path(folder_path):
    """Add a given folder path to Python's sys.path if it's not already included."""
    if folder_path not in sys.path:
        sys.path.append(folder_path)
        return "Added '{}' to sys.path".format(folder_path)
    else:
        return "'{}' already in sys.path".format(folder_path)