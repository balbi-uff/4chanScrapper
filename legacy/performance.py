from legacy_img_scrapper import sync_main
from legacy.async_img_scrapper import async_main

if __name__ == "__main__":
    link_to_test = "https://boards.4chan.org/wg/thread/7830569"
    print("beginning async_main")
    print("ASYNCRONOUS => time elapsed:{}".format(async_main(link_to_test)))
    print("end async_main")
    
    print("beginning sync_main")
    print("SYNCRONOUS => time elapsed:{}".format(sync_main(link_to_test)))
    print("end sync_main")
    
    