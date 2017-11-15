#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os
import urllib
from urllib.request import urlopen

INDEX_DIRECTORY = './index/'

def main():

    tree = ET.parse('arxiv.html')
    root = tree.getroot()

    for div in root.iter('div'):
        category = div.attrib['id']
        category_directory = INDEX_DIRECTORY+category

        if not os.path.exists(category_directory):
            os.makedirs(category_directory)
        print(category_directory)

        for a in div.iter('a'):
            category_name = a.attrib['href'].split('/')[2]
            index_filename = category_name + "_" + a.text + ".xml"

            url = 'http://export.arxiv.org/api/query?search_query=all:'+ category_name +'&start=0&max_results=500'
            data = urllib.request.urlopen(url).read()

            final_path = category_directory+'/'+index_filename
            with open(final_path, 'wb') as query_file:
                query_file.write(data)

            print(final_path)
           

if __name__ == "__main__":
    main()