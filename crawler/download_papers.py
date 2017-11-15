#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET
import urllib
from urllib.request import urlopen
import os

INDEX_PATH = "./index/"
PAPERS_PATH = "./papers/"

LABELS = set()

def download_index_file(path_file):
    print("Downloading:", str(path_file))
    tree = ET.parse(str(path_file))
    root = tree.getroot()

    file_name = PAPERS_PATH + str(path_file.parents[0]) + "/"
    if not os.path.exists(file_name):
        os.makedirs(file_name)

    with open(file_name + 'categories.txt', 'r') as labels_file:
        for c in labels_file.readlines():
            LABELS.add(c.strip('\n'))

    for entry in root.iter('{http://www.w3.org/2005/Atom}entry'):

        id = ''
        link_pdf = ''
        categories = []
        for c in entry:        
            if c.tag == '{http://www.w3.org/2005/Atom}id':
                id = c.text
            
            if c.tag == '{http://www.w3.org/2005/Atom}link':
                if 'type' in c.attrib and c.attrib['type'] == 'application/pdf':
                    link_pdf = c.attrib['href']

            if c.tag == '{http://www.w3.org/2005/Atom}category':
                label = c.attrib['term'].strip('\n')
                print(label)
                if label in LABELS:
                    print(label)
                    categories.append(label)


        print("ID: ", id)
        print('link: ', link_pdf)
        print("Categories: ")
        for cat in categories:
            print("\t Category:", cat)
                
        final_file_name = file_name + link_pdf.split('/')[-1]

        final_file_name_pdf = final_file_name + ".pdf"
        final_file_name_lab = final_file_name + ".lab"

        if not os.path.exists(final_file_name_pdf):

            print(link_pdf, "To:" , final_file_name)

            try:
                data = urllib.request.urlopen(link_pdf).read()

                with open(final_file_name_pdf, 'wb') as paper_file:
                    paper_file.write(data)
            except urllib.error.HTTPError as err:
                if err.code == 403:
                    print("Error HTTP 403 ¿Te han baneado de Arxiv?")
                else:
                    raise        
        else:
            print(id, " PDF already in disc, Skipping:", final_file_name)

        # if not os.path.exists(final_file_name_lab):
        with open(final_file_name_lab, 'w') as paper_labels:
            for cat in categories:
                paper_labels.write(cat+"\n")
        #else:
        #    print(id, " Labels file already in disc, Skipping:", final_file_name)


def download_index(path_file):
    print("Entering directory:" + str(path_file))
    if path_file.is_dir():
        for p in path_file.iterdir():
            if p.is_dir():
                download_index(p)
            else:
                download_index_file(p)
    else:
        download_index_file(path_file)

def main():
    download_index(Path(INDEX_PATH))

if __name__ == "__main__":
    main()