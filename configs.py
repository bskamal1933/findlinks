import os


def get_proj_path():
    """
    This returns the project path till \findlinks

    You can add this to your required path :
    proj_path + '\tests\file'
    """
    cwd = os.getcwd()
    path = ''
    cwd = cwd.split('\\')
    for item in cwd:
        if item == 'C:':
            path = 'C:'
        elif item != 'findlinks':
            path = path + "\\" + item
        else:
            path = path + "\\" + item
            break
    return path
