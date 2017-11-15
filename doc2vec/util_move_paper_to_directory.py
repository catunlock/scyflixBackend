import os
from shutil import copyfile

f_input = 'computer_science'
f_output = f_input + '_classified'


def main():
    for file in os.listdir(f_input):
        file_lab = f_input + '_labels' + '/' + file[:-4] + '.lab'
        if os.path.isfile(file_lab):
            with open(file_lab, 'r') as f_lab:
                labels = f_lab.readlines()
                for l in labels:
                    l = l.strip('\n')
                    outdir = f_output + '/' + l
                    if not os.path.exists(outdir):
                        os.makedirs(outdir)

                    source = f_input + '/' + file
                    dest = outdir + '/' + file
                    print(source, ' ====>> ', dest)
                    copyfile(source, dest)

if __name__ == "__main__":
    main()
