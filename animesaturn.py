import concurrent.futures
import configparser
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class AnimeSaturn:
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    anime_page_url = ""
    download_path = "downloads/"
    link_list = list()
    season_num = 0
    all_ep = {}
    concurrent_downloads_limit = -1

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.import_config()
        self.selected_anime()

    @staticmethod
    def check_path(path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def import_config(self):
        if self.config["DEFAULT"].get("anime_page_url") is (None or ""):
            print("You need to specify target anime page URL. Aborting...")
        else:
            self.anime_page_url = self.config["DEFAULT"]['anime_page_url']

        if self.config["DEFAULT"].get("concurrent_downloads_limit") is (None or ""):
            self.concurrent_downloads_limit = 1
        else:
            self.concurrent_downloads_limit = int(self.config["DEFAULT"]['concurrent_downloads_limit'])

    def selected_anime(self):
        ep_list = list()
        mutex = False
        new_r = requests.get(url=self.anime_page_url, params={})
        pastebin_url = new_r.text
        parsed_html = BeautifulSoup(pastebin_url, "html.parser")
        while mutex:
            time.sleep(0.5)
        mutex = True
        anime_ep = parsed_html.find_all('div', attrs={'class': 'btn-group episodes-button episodi-link-button'})
        self.link_list.clear()
        for dim in anime_ep:
            episode = dim.find('a')['href']
            episode = episode + "§%d" % self.season_num
            ep_list.append(episode)
        mutex = False

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(ep_list)) as pool:
            futures = [pool.submit(self.one_link, ep) for ep in ep_list]
            concurrent.futures.wait(futures)

        self.downloader()
        ep_list.clear()

    def one_link(self, ep):
        x = ep.split("§")
        new_r = requests.get(url=x[0], params={})
        pastebin_url = new_r.text
        parsed_html = BeautifulSoup(pastebin_url, "html.parser")
        anime_page = parsed_html.find('div', attrs={'class': 'card bg-dark-as-box-shadow text-white'})
        is_link = anime_page.find('a')['href']
        if 'watch' in is_link:
            episode = is_link + '&s=alt'
            self.all_ep[episode] = x[1]
            self.link_list.append([episode, int(x[0].split("-")[-1])])

    def downloader(self):
        download_link = list()

        if not os.path.isdir(self.download_path):
            os.makedirs(self.download_path)

        print("Found %d episodes" % len(self.link_list))
        episodes = []
        while True:
            try:
                target_episodes = input("Select 'all' or range (1:%d) " % len(self.link_list)).split(":")
                if "all" in (target_episodes[0].lower()):
                    start, finish = 1, len(self.link_list)
                elif len(target_episodes) == 1:
                    start, finish = int(target_episodes[0]), int(target_episodes[0])
                else:
                    start, finish = int(target_episodes[0]), int(target_episodes[1])
                if 0 < finish <= len(self.link_list) and 0 < start <= len(self.link_list):
                    break
                print("Range not valid. Try again.")
            except ValueError:
                print("Range not valid. Try again.")
        for episode_data in self.link_list:
            if start <= episode_data[1] <= finish:
                source_html = requests.get(episode_data[0]).text
                try:
                    mp4_link = re.findall("file: \"(.*)\",", source_html)
                except IndexError:
                    mp4_link = ""
                episodes.append(mp4_link)
        print("\n")
        for i, ep in enumerate(sorted(episodes)):
            download_link.append([ep[0], self.link_list[i]])
        if self.concurrent_downloads_limit == -1:
            limit = len(download_link)
        else:
            limit = self.concurrent_downloads_limit
        with concurrent.futures.ThreadPoolExecutor(max_workers=limit) as pool:
            pool.map(self.download, download_link)
        self.link_list.clear()

    def download(self, url):
        url, ll = url
        file_name = url.split("/")[-1]
        self.check_path(os.path.join(self.download_path, file_name.split("_")[0]))
        with open(os.path.join(self.download_path, file_name.split("_")[0], file_name), "wb"):
            response = requests.get(url, stream=True, headers={"Referer": ll[0]})
            with tqdm.wrapattr(open(os.path.join(self.download_path, file_name.split("_")[0], file_name), "wb"),
                               "write", desc=url.split('/')[-1],
                               total=int(response.headers.get('content-length', 0))) as fout:
                for chunk in response.iter_content(chunk_size=4096):
                    fout.write(chunk)


if __name__ == "__main__":
    AnimeSaturn()
