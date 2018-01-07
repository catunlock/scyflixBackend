#! /usr/bin/env python
 
import sys
import os
import argparse
import pyPdf
import os

def extractFirstPage(file_path, destination):
    output_filepath = file_path[:-4] + "X.pdf"
    print('Extracted first page from ' + file_path + ' in ' + output_filepath[:-5] + '.png')

    pdf_in = pyPdf.PdfFileReader(open(file_path, 'r'))
    pdf_out = pyPdf.PdfFileWriter()

    pdf_out.addPage(pdf_in.getPage(0))
    out_stream = open(os.path.expandvars(os.path.expanduser(output_filepath)), "wb")

    pdf_out.write(out_stream)
    out_stream.close()

    # convierto en jpg y elimino el pdf residuo
    os.system("convert -density 300 " + output_filepath + " " + output_filepath[:-5] + ".png")
    os.system("rm " + output_filepath)
    os.system("mv " + output_filepath[:-5] + ".png " + destination)
 
def main():

    if (len(sys.argv) < 3):
        print ('Usage: extractFirstPage XXXXXX.pdf destination')
        exit()


    extractFirstPage(sys.argv[1], sys.argv[2])

 
if __name__ == '__main__':
    main()