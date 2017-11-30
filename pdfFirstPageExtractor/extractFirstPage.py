#! /usr/bin/env python
 
import sys
import os
import argparse
import pyPdf
import os
 
 
def main():

    if (len(sys.argv) < 3):
        print ('Usage: extractFirstPage XXXXXX.pdf destination')
        exit()
    output_filepath = sys.argv[1][:-4]+"X.pdf"
    print ('Extracted first page from '+ sys.argv[1] + ' in '+output_filepath[:-5]+'.jpg')

    pdf_in = pyPdf.PdfFileReader(open(sys.argv[1],'r'))
    pdf_out = pyPdf.PdfFileWriter()
        
    pdf_out.addPage(pdf_in.getPage(0))
    out_stream = open(os.path.expandvars(os.path.expanduser(output_filepath)), "wb")

    pdf_out.write(out_stream)
    out_stream.close()

    #convierto en jpg y elimino el pdf residuo
    os.system("convert "+output_filepath+" "+output_filepath[:-5]+".jpg")
    os.system("rm "+output_filepath)
    os.system("mv "+output_filepath[:-5]+".jpg "+ sys.argv[2])
 
if __name__ == '__main__':
    main()