import sys

from scrapper.scrapper_methods import download_files_from_thread

MINIMUM_ARGUMENTS_THRESHOLD = 2

def get_arguments_from_command_line():
    """
    Gets arguments from command line and returns them as a list.
    """
    return sys.argv

def is_manual_mode_trigger(argument):
    return argument.startswith("-m")


def has_minimum_argument_thresold(arguments):
    return len(arguments) >= MINIMUM_ARGUMENTS_THRESHOLD


def manual_mode_download():
    """
    Manual mode is triggered when -m is passed as argument.
    """
    print("Manual mode is not yet implemented.")
    return 0


if __name__ == '__main__':
    arguments = get_arguments_from_command_line()
    try:
        if is_manual_mode_trigger(arguments[1]):
            manual_mode_download()
        elif has_minimum_argument_thresold(arguments):
            thread_link = arguments[1]
            download_path = arguments[2]
            download_files_from_thread(thread_link, download_path)
        else:
            raise Exception("Not enough arguments.")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
