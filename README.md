# Simple bulk video downloader for Reddit

## Features
- Download last X videos from Y subreddit
- Stitch together audio and video
- Vids are saved in subfolder "videos" in MP4 format.
- No need for setting up API




## Installation for Windows
I assume you already have Python installed and added to your PATH. If not go to: https://www.python.org/downloads/

Create folder for project.
```bash
mkdir SimpleRedditDownloader && cd SimpleRedditDownloader
```

Download repo using.
```bash
git clone https://github.com/GLB-RT/SimpleRedditDownloader.git && cd SimpleRedditDownloader
```

Create virtual enviroment using venv.
 ```bash
py -m venv .venv
```
Activate your venv.
```bash
call .venv/Scripts/Activate
```
Download all packagages in req.txt and wait untill everything is downloaded and installed.
```bash
pip install -r req.txt
```
Now you can run script.
```bash
python app.py
```
## Authors

- [@GLB-RT](https://github.com/GLB-RT)


## Acknowledgements

 - [learncpp](https://www.learncpp.com/)


