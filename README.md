# Animesaturn-Downloader

Lite utility to download an entire anime season using its page URL.
Tested on Windows only.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

### Installation using virtualenv

- Install VS build tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Install virtualenv using pip `pip install virtualenv`
- Create a virtual env `python -m virtualenv venv`
- Activate your virtual env `venv/Scripts/activate.bat`
- Install dependencies `pip install -r requirements.txt`

### Use the downloader

- Configure the file config.ini with anime page URL and concurrent downloads limit.
- Run using `python ASD.py`