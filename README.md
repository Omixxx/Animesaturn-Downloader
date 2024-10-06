# Animesaturn-Downloader

**Lite utility to download an entire anime season using its page URL.**  
Tested on **Windows** only.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Prerequisites

1. **Install Visual Studio Build Tools**  
   Download and install the Visual C++ Build Tools from the [official site](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

2. **Install virtualenv using pip**  
   Run the following command to install `virtualenv`:

   ```bash
   pip install virtualenv
   ```

## Setup

1. **Create and activate a virtual environment**

   On **Windows**:

   ```bash
   python -m virtualenv venv
   venv\Scripts\activate.bat
   ```

   If you're using the **fish** shell:

   ```bash
   venv\Scripts\activate.fish
   ```

2. **Install the required dependencies**

   Run the following command to install all dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create your configuration file**

   Copy the example configuration file and rename it:

   ```bash
   cp config.ini.example config.ini 
   ```

## Configuration

The `config.ini` file contains the necessary settings for the downloader. Currently, it supports the following parameters:

1. **`anime_url`** → The URL of the anime series' main page (not individual streaming pages).
2. **`concurrent_download_limit`** → The maximum number of concurrent downloads allowed.

Make sure to update these fields according to your requirements.

## Usage

To start downloading an anime season, simply run:

```bash
python ASD.py
```

The downloader will automatically fetch and download all episodes of the anime series from the provided URL.
