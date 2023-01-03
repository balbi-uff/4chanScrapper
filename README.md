# 4chan Media Scrapper
#### This program asynchronously scrapes a single thread from **4chan.org**, downloading **every image and video** in the thread, according to your filters.

### Requirements
> `pip install -r "requirements.txt"`

Every other package used is included in Python 3.8+

### Usage

This program works in two separate ways, the automatic mode and the manual mode. The automatic requires the insertion of the thread URL, while the manual requires the insertion of the thread link (mandatory) and the download path, respectively.

**Auto mode**
<br>
This is the default mode, and it is the easiest to use. Just run the program with the thread link and download_path. The program will automatically download the files in the thread, according to your filters.
<br>
```commandline
python Fscrapper.py thread_link download_path
```

**Manual mode**
<br>
Make sure to use the `-m` flag to enable the manual mode. Followed by the thread link and the download path.
<br>
Using manual mode, you may decide (or not) to insert minimum and maximum resolution filters for the downloaded files.
<br>

```commandline
python Fscrapper.py -m thread_link download_path --min-res x y --max-res x y
```

> More implementations are planned for the future, they will expand the difference between the two modes.

### Disclaimer
This program is intended for educational purposes only. I am not responsible for any misuse of this program.

###### v2.0 - Flow refactoring
