# 4chan Media Scrapper
#### This program asynchronously scrapes a single thread from **4chan.org**, downloading **every image and video** in the thread.

### Requirements
> `pip install -r "requirements.txt"`

Every other package used is included in Python 3.8+

### Usage
- For now, you can only scrape a single thread. You may do this by executing the program with the following command:
    ```shell:
    python 4chanScrapper.py -l <thread_link> -p <path_to_save_images>
    ```
### Optional features

- You may set the minimum of maximum resolution of the images to be downloaded by typing how many of these you want in the command line:
    ```shell:
    -min_x <min_x>
    -min_y <min_y>
    -max_x <max_x>
    -max_y <max_y>
    ```
    where `<min_x>` and `<min_y>` are the minimum resolution of the images in the x and y direction, and `<max_x>` and `<max_y>` are the maximum resolution of the images in the x and y direction.
    
- You may automatically trigger the creation of a folder by typing 
    ```shell:
    -name <folder_name>
    ```
    where `<folder_name>` is the name of the folder to be created.
    
- Stable in Python 3.8.5
### Disclaimer

- This is a very simple program. If the site changes its frontend infrastructure, this program may stop working.

### Example
```shell:
    python 4chanScrapper.py -l "https://boards.4chan.org/wg/thread/7830569" -p "C://Users/username/Desktop"
```

###### v1.2 - CLI options - stable.
