# 4chanScrapper
#### This program asynchronously scrapes threads from **4chan.org**, downloading **every image and video** in the thread.
<br>

### Requirements
> `pip install -r "requirements.txt"`

Every other package used is included in Python 3.8+

### Usage
- For now, you can only scrape a single thread. You may do this executing the program with the following command:
    ```shell:
    python 4chanScrapper.py "thread_url" "path"
    ```
- You may trigger the automatic creation of a folder if you add the `--create_folder` flag to the command.
- It was tested successfully in Python 3.8.5
### Disclaimer

- This is a very simple program. If the site changes its frontend infrastructure, this program may stop working.

### Example
```shell:
    python 4chanScrapper.py "https://boards.4chan.org/wg/thread/7830569" "C://Users/username/Desktop"
```

###### v1.1 - create folder and progress update - stable.