"""Provides a scripting component.
    Inputs:
        folder_path: The directory path to add to sys.path.
        add_to_path: Boolean to control whether to add folder_path to sys.path.
    Output:
        message: A message about the action taken or not taken."""

import sys

if add_to_path:
    if folder_path not in sys.path:
        sys.path.append(folder_path)
        message = "Added '{}' to sys.path".format(folder_path)
    else:
        message = "'{}' already in sys.path".format(folder_path)
else:
    message = "Add to path is False. No action taken."