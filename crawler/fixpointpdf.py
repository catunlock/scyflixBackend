import os

path_pdf = "/home/sunlock/computer_science_magpie/"

for f in os.listdir(path_pdf):
    if not f[-4:] == '.pdf':
        os.rename(path_pdf + f, path_pdf + f[:-3] + '.pdf')
