from shutil import ExecError
from wave import Error
from async_img_scrapper import async_main
import sys

if __name__ == "__main__":
    try:
        arguments = sys.argv
        if len(arguments) == 1:
            raise Error
        link_to_test = arguments[1]
        path = arguments[2]
        create_folder = True if "--create_folder" in arguments else False
        execution_time = async_main(link_to_test, path, create_folder)
        print("Process ended. Time elapsed:{}".format(execution_time))
    except Error:
        print("Please, insert link to download as argument")
        print("Example: python 4chanScrapper.py \"https://boards.4chan.org/wg/thread/7830569\" \"C://Users/username/Desktop\"" )
        print("Exiting...")
        sys.exit(1)
    
    except Exception as error_name:
        print(f"This happened => {error_name}")
        print("Exiting...")
        sys.exit(1)