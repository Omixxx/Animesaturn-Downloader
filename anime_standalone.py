# importing the requests library
import requests
import os
import signal
import re
import time
import concurrent.futures
from tqdm import tqdm
import init
import classes

def download(url):
    file_name = url.split("/")[-1]
    classes.check_Path(os.path.join(init.config["DEFAULT"]['download_path'],file_name.split("_")[0]))
    with open(os.path.join(init.config["DEFAULT"]['download_path'],file_name.split("_")[0],file_name), "wb") as file:
        response = requests.get(url, stream=True)
        with tqdm.wrapattr(open(os.path.join(init.config["DEFAULT"]['download_path'],file_name.split("_")[0],file_name), "wb"), "write", miniters=1, desc=url.split('/')[-1], total=int(response.headers.get('content-length', 0))) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)
        file.write(response.content)

def downloader():
    #creo un file vuoto, se presente sovrascrivo
    classes.check_Path(str(init.config["DEFAULT"]['download_path'])) #verifico che path esista
    print("Rilevati %d episodi"%len(init.list_link))
    episodes = []
    while True:
        try:
            wantedEps = input("Dammi Range Episodi (1:%d) "%len(init.list_link)).split(":")
            if("all" in (wantedEps[0].lower())):
                start, finish = 1, len(init.list_link)
            elif(len(wantedEps) == 1):
                start, finish = int(wantedEps[0]), int(wantedEps[0])
            else:
                start, finish = int(wantedEps[0]), int(wantedEps[1])
            if(start > 0 and finish > 0 and finish <= len(init.list_link) and start <= len(init.list_link)):
                break
            print("Invalido!")
        except ValueError:
            print("Invalido!")
    for episodedata in init.list_link:
        #if(start <= int(episodedata[1]) <= finish):
        sourcehtml = requests.get(episodedata).text
        source = re.findall("file: \"(.*)\",",sourcehtml)
        try:
            mp4_link = source[0]
        except IndexError:
            mp4_link = ""
        episodes.append(mp4_link)
    print("\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(episodes)) as pool:
        pool.map(download, episodes)
    init.list_link.clear()
#riordino correlati e  selezionato in base alla data di uscita

def main():
    init.file_type = 1
    signal.signal(signal.SIGTERM, classes.sig_handler)
    signal.signal(signal.SIGINT, classes.sig_handler)
    classes.import_config()
    name = input("nome:")
    classes.search(name)

if __name__ == "__main__":
    main()
