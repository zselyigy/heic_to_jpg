import os
import subprocess
import sys
import zipfile as zip
import logging


def folders(args):
    i = 0
    directory = args.replace('\\', '/')
    directorylist = [directory]
    while i < len(directorylist):
        print(i)
        szar = [f"{directorylist[i]}/{f}" for f in os.listdir(directorylist[i]) if os.path.isdir(f"{directorylist[i]}/{f}")]
        for darab in szar:
            directorylist.append(darab)
        i += 1
    return directorylist
    
def transform(directorylist):
    for directory in directorylist:
        files = [f for f in os.listdir(directory) if f.lower().endswith('.heic') or f.lower().endswith('.heif')]
        if len(files) != 0:
            for filename in files:
                command = rf'.\.venv\Scripts\heif-convert.exe -o {filename[:-5]} -p "{directory}" -q 95 "{directory}/{filename}"'
                #
                try:
                    subprocess.run(command, shell=True, check=True)
                    logging.info(f"{filename} ---> {filename[:-5]}.jpg ({directory})")
                except:
                    print(f"Error converting {filename}")

            # Select the compression mode ZIP_DEFLATED for compression
            # or zipfile.ZIP_STORED to just store the file
            compression = zip.ZIP_DEFLATED
            print(f"{directory}/HEIC.zip")
            zf = zip.ZipFile(f"{directory}/HEIC.zip", mode="w")

            for file_to_write in files:
                try:
                    print(f"{directory}/{file_to_write}")
                    # Add file to the zip file
                    # first parameter file to zip, second filename in zip
                    zf.write(f"{directory}/{file_to_write}", file_to_write, compress_type=compression, compresslevel=0)
                    os.remove(f"{directory}/{file_to_write}")

                except FileNotFoundError as e:
                    print(f' *** Exception occurred during zip process - {e}')
            logging.info(f"{directory} HEIC files zipped")
            zf.close()

def main():
    args = sys.argv[1]
    logging.basicConfig(filename="latest.log", level=logging.INFO, filemode='w',format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    directorylist = folders(args)
    transform(directorylist)

if __name__ == "__main__":
    main()