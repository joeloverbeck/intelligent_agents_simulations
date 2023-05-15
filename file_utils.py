import os

from errors import DirectoryDoesntExistError, FileDoesntExistError


def ensure_full_file_path_exists(simulation_name, file_name):
    path = "simulations"

    if not os.path.exists(path):
        raise DirectoryDoesntExistError(f"The path '{path}' doesn't exist.")

    path = path + f"/{simulation_name}"

    if not os.path.exists(path):
        raise DirectoryDoesntExistError(f"The path '{path}' doesn't exist.")

    full_path = path + f"/{file_name}.json"

    if not os.path.isfile(full_path):
        raise FileDoesntExistError(f"The file '{full_path}' doesn't exist.")

    return full_path
