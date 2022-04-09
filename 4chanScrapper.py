from shutil import ExecError
from wave import Error
from async_img_scrapper import async_main
import sys

arguments_names = { name : None for name in
    [
        "link",
        "path",
        "forced_name",
        "force_resolution",
        "min_res_x",
        "min_res_y",
        "max_res_x",
        "max_res_y",
        "create_folder",
    ]
}
if __name__ == "__main__":
    try:
        
        arguments_values = sys.argv
        
        for value_address in range(arguments_values.keys()):
            arguments_names[arguments_names.keys()[value_address]] = arguments_values[value_address]

        if len(arguments_values) < 1:
            raise Error
        
    # NAO TA PREVENDO CASOS EM QUE TIPO O CARA BOTA A RESOLUCAO MAS N O NOME TLGD RESOLVE ISSO AE VLW

        execution_time = async_main(link=               arguments_names["link"], 
                                    path=               arguments_names["path"], 
                                    forced_name=        arguments_names["forced_name"], 
                                    force_resolution=   arguments_names["force_resolution"], 
                                    min_res_x=          arguments_names["min_res_x"], 
                                    min_res_y=          arguments_names["min_res_y"], 
                                    max_res_x=          arguments_names["max_res_x"], 
                                    max_res_y=          arguments_names["max_res_y"], 
                                    create_folder=      arguments_names["create_folder"])
        print("Process ended. Time elapsed:{}".format(execution_time))
    except Error:
        print("Please, insert link to download as argument")
        print("Example: python 4chanScrapper.py \"https://boards.4chan.org/wg/thread/7830569\" \"C:\\Wallpapers\\" )
        print("Exiting...")
        sys.exit(1)
    
    except Exception as error_name:
        print(f"This happened => {error_name}")
        print("Exiting...")
        sys.exit(1)