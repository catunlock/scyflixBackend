import urllib
from urllib.request import urlopen
import os

path_arxiv = "https://arxiv.org/pdf/"
download_path = "/home/sunlock/computer_science_magpie/"

def download_paper(id_paper):
    download_file_path = download_path + id_paper + '.pdf'
    if not os.path.exists(download_file_path):

        print("Downloading", id_paper)

        try:
            data = urllib.request.urlopen(path_arxiv + id_paper).read()

            with open(download_file_path, 'wb') as paper_file:
                paper_file.write(data)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                print("Error HTTP 404 Paper not found.")
            elif err.code == 403:
                print("Error HTTP 403 ¿Te han baneado de Arxiv?")
            else:
                raise
    else:
        print(id, " PDF already in disc, Skipping:", id_paper)


def main():
    with open("notyetdownloaded.txt", 'r') as file_pendents:
        for id_paper in file_pendents.readlines():
            download_paper(id_paper)


if __name__ == "__main__":
    main()