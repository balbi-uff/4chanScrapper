from shutil import ExecError
from wave import Error
from async_img_scrapper import async_main
import sys


LINK = "-l"
PATH = "-p"
NAME = "-name"
MINIMUM_RESOLUTION_X_AXIS = "-min_x"
MINIMUM_RESOLUTION_Y_AXIS = "-min_y"
MAXIMUM_RESOLUTION_X_AXIS = "-max_x"
MAXIMUM_RESOLUTION_Y_AXIS = "-max_y"
CREATE_FOLDER_FLAG_NAME = "-cf"


ACCEPTED_ARGUMENT_NAMES = { name : None for name in
    [
        LINK,
        PATH,
        NAME,
        MINIMUM_RESOLUTION_X_AXIS,
        MINIMUM_RESOLUTION_Y_AXIS,
        MAXIMUM_RESOLUTION_X_AXIS,
        MAXIMUM_RESOLUTION_Y_AXIS,
    ]
}
if __name__ == "__main__":
    try:
        inputed_args = [
            LINK, 'https://boards.4chan.org/wg/thread/7886651',
            PATH, 'C://Wallpapers',
            NAME, "TEST-NAME-1",

        ]

        #inputed_args = [LINK, "https://boards.4chan.org/wg/thread/7887741"]

        #inputed_args = sys.argv
        
        "Links next argument with previous var (Except for resolution matters). It's confuse, but once you get it, it's easy."

        for arg in inputed_args:
            if arg in ACCEPTED_ARGUMENT_NAMES.keys():
                ACCEPTED_ARGUMENT_NAMES[arg] = inputed_args[inputed_args.index(arg)+1]
        
        if len(inputed_args) < 1:
            raise Error
        

        execution_time = async_main(
                                link=               ACCEPTED_ARGUMENT_NAMES[LINK], 
                                path=               ACCEPTED_ARGUMENT_NAMES[PATH], 
                                forced_name=        ACCEPTED_ARGUMENT_NAMES[NAME], 
                                min_res_x=          int(ACCEPTED_ARGUMENT_NAMES[MINIMUM_RESOLUTION_X_AXIS]) if ACCEPTED_ARGUMENT_NAMES[MINIMUM_RESOLUTION_X_AXIS] else 0, 
                                min_res_y=          int(ACCEPTED_ARGUMENT_NAMES[MINIMUM_RESOLUTION_Y_AXIS]) if ACCEPTED_ARGUMENT_NAMES[MINIMUM_RESOLUTION_Y_AXIS] else 0, 
                                max_res_x=          int(ACCEPTED_ARGUMENT_NAMES[MAXIMUM_RESOLUTION_X_AXIS]) if ACCEPTED_ARGUMENT_NAMES[MAXIMUM_RESOLUTION_X_AXIS] else 99999, 
                                max_res_y=          int(ACCEPTED_ARGUMENT_NAMES[MAXIMUM_RESOLUTION_Y_AXIS]) if ACCEPTED_ARGUMENT_NAMES[MAXIMUM_RESOLUTION_Y_AXIS] else 99999,
                                )
        print("Process ended. Time elapsed:{}".format(execution_time))
    
    except Error:
        print("Please, insert link to download as argument")
        print("Example: python 4chanScrapper.py \"https://boards.4chan.org/wg/thread/7830569\" \"C:\\Wallpapers\\" )
        print("Exiting...")
        sys.exit(1)
    
    # except Exception as error_name:
    #     print(f"This happened => {error_name}")
    #     print("Exiting...")
    #     sys.exit(1)