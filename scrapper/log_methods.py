from rich.console import Console

log_console = Console()
error_console = Console(stderr=True, style="bold red")


def log_progress_message(message):
    log_console.log(message, style="blue")


def log_error_message(error_message):
    error_console.log(error_message)


def log_manual_mode_trigger_message():
    log_console.log("Manual mode trigger activated!", style="bold green")


def log_automatic_mode_trigger_message():
    log_console.log("Automatic mode trigger activated!", style="bold green")


def log_setting_resolution_message(message, res_x, res_y):
    log_console.log(message + ":", style="italic green", end="")
    log_console.log(str(res_x) + "x" + str(res_y), style="bold green")

