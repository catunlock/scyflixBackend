from pymongo import MongoClient
import os

download_path = "/home/sunlock/computer_science_magpie/"
selecteds_path = "/home/sunlock/selected_papers/"

def move_paper(paper_id):
    os.rename(download_path + paper_id + '.pdf', selecteds_path + paper_id + 'pdf')


def main():
    client = MongoClient()
    db = client.database

    for paper in db.papers.find():
        print(paper['id'])
        move_paper(paper['id'])


if __name__ == "__main__":
    main()