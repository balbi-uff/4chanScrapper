import sys
from rich.markdown import Markdown
from scrapper.log_methods import *
from scrapper.scrapper_methods import download_files_from_thread

MINIMUM_ARGUMENTS_THRESHOLD = 1
HELP_TRIGGERS = ["-h", "--help"]


def get_arguments_from_command_line():
    """
    Gets arguments from command line and returns them as a list.
    """
    return sys.argv


def is_manual_mode_trigger(argument):
    return argument.startswith("-m")


def has_minimum_argument_threshold(arguments):
    return len(arguments) >= MINIMUM_ARGUMENTS_THRESHOLD


def manual_resolution_setting_simple(arguments):
    """
    Checks if resolution is set in manual mode - simple.
    """
    return "--resolution" in arguments


def manual_resolution_setting_full_config(arguments):
    """
    Checks if resolution is set in manual mode - full config and not in simple.
    """
    return (
        "--max-res" in arguments or "--min-res" in arguments
    ) and not manual_resolution_setting_simple(arguments)


def get_resolution_from_arguments_standart(res_arguments, resolution_trigger_str):
    """
    Abstract method for getting resolution from arguments.
    """
    resolution_trigger_index = res_arguments.index(resolution_trigger_str)
    x_resolution = int(res_arguments[resolution_trigger_index + 1])
    y_resolution = int(res_arguments[resolution_trigger_index + 2])
    return x_resolution, y_resolution


def get_resolution_from_arguments_simple(res_arguments):
    """
    Gets resolution from arguments.
    """
    return get_resolution_from_arguments_standart(res_arguments, "--resolution")


def define_resolution_full_config(res_args, resolution_trigger_str):
    # Obtain minimum resolution
    if resolution_trigger_str in res_args:
        x, y = get_resolution_from_arguments_standart(res_args, resolution_trigger_str)
    else:
        x, y = None, None
    return x, y


def get_resolution_from_arguments_full_config(res_arguments):
    """
    Gets resolution from arguments.
    """

    # Obtain minimum resolution
    min_x_res, min_y_res = define_resolution_full_config(res_arguments, "--min-res")

    # Obtain maximum resolution
    max_x_res, max_y_res = define_resolution_full_config(res_arguments, "--max-res")

    return min_x_res, min_y_res, max_x_res, max_y_res


def manual_mode_download(arguments):
    """
    Manual mode is triggered when -m is passed as argument.

    Expected arguments:
    # Full command example:
    $ python FchanScrapper.py -m thread_link download_path --resolution 1920 1080
                [0]            [1] [2]         [3]              [4]      [5] [6]

    $ python FchanScrapper.py -m thread_link download_path --min-res 1920 1080 --max-res 1920 1080
                [0]           [1]    [2]         [3]              [4] [5]  [6]    [7]     [8]  [9]

    """

    manual_mode_arguments = arguments[2:]
    if manual_resolution_setting_simple(manual_mode_arguments):
        x_resolution, y_resolution = get_resolution_from_arguments_simple(
            manual_mode_arguments
        )
        log_setting_resolution_message(
            "Resolution limits set to", x_resolution, y_resolution
        )

        return download_files_from_thread(
            manual_mode_arguments[0],
            manual_mode_arguments[1],
            min_x_res=x_resolution,
            min_y_res=y_resolution,
            max_x_res=None,
            max_y_res=None,
        )
    if manual_resolution_setting_full_config(manual_mode_arguments):
        [min_x, min_y, max_x, max_y] = get_resolution_from_arguments_full_config(
            manual_mode_arguments
        )
        log_setting_resolution_message("Minimum accepted resolution", min_x, min_y)
        log_setting_resolution_message("Maximum accepted resolution", max_x, max_y)

        return download_files_from_thread(
            manual_mode_arguments[0],
            manual_mode_arguments[1],
            min_x_res=min_x,
            min_y_res=min_y,
            max_x_res=max_x,
            max_y_res=max_y,
        )
    else:
        raise Exception(
            "Resolution not set. Please set resolution with --resolution <resolution-x> <resolution-y> or "
            "type -h for help."
        )


def display_help():
    with open("README.md", "r+") as help_file:
        log_console.print(Markdown(help_file.read()))
    sys.exit(0)


def is_help_trigger(arguments):
    return any([i.lower() in arguments for i in HELP_TRIGGERS])


if __name__ == "__main__":
    log_console.print("For help use the arguments -h or --help", style="bold red underline")
    command_line_arguments = get_arguments_from_command_line()
    try:
        if is_help_trigger(command_line_arguments):
            display_help()
        elif is_manual_mode_trigger(command_line_arguments[1]):
            manual_mode_download(command_line_arguments)

        # Enters automatic mode

        elif has_minimum_argument_threshold(command_line_arguments):
            thread_link = command_line_arguments[1]

            if len(command_line_arguments) == 2:
                download_path = None
            else:
                download_path = command_line_arguments[2]
            download_files_from_thread(thread_link, download_path)
        else:
            raise Exception("Not enough arguments.")
        sys.exit(0)
    except IndexError as e:
        log_error_message("Please insert arguments correctly while on manual mode.")

    except Exception as e:
        log_error_message(e)

    sys.exit(1)
