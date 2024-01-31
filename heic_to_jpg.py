import os
import subprocess
import sys
import zipfile as zip
import logging
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog

def gui():
    global label
    #Set the theme and color options
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    #Create root object
    root = ctk.CTk()
    #Set GUI title
    root.title("HEIC to jpg converter")
    #Set GUI size to zoomed
    root.after(1, lambda: root.state("zoomed"))
    
    fb = ctk.CTkButton(master=root, text="Choose file", command=get_file).pack()
    db = ctk.CTkButton(master=root, text="Choose directory", command=get_directory).pack()
    label = ctk.CTkLabel(root, text="File or directory path will appear here.")
    label.pack()
    root.mainloop()
    

def folders():
    i = 0
    directory = dirs.replace('\\', '/')
    directorylist = [directory]
    while i < len(directorylist):
        print(i)
        szar = [f"{directorylist[i]}/{f}" for f in os.listdir(directorylist[i]) if os.path.isdir(f"{directorylist[i]}/{f}")]
        for darab in szar:
            directorylist.append(darab)
        i += 1
    return directorylist
    
def convert_rec(directorylist):
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

def convert(directory):
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

def convert_f(file):
    command = rf'.\.venv\Scripts\heif-convert.exe -o {file[:-5]} -p "{file}" -q 95 "{file}"'
    #
    try:
        subprocess.run(command, shell=True, check=True)
        logging.info(f"{file} ---> {file[:-5]}.jpg)")
    except:
        print(f"Error converting {file}")

def convert_fs(filelist):
    for file in filelist:
        for filename in filelist:
            command = rf'.\.venv\Scripts\heif-convert.exe -o {filename[:-5]} -p "{os.path.dirname(filename)}" -q 95 "{filename}"'
            try:
                subprocess.run(command, shell=True, check=True)
                logging.info(f"{filename} ---> {filename[:-5]}.jpg")
            except:
                print(f"Error converting {filename}")

        # Select the compression mode ZIP_DEFLATED for compression
        # or zipfile.ZIP_STORED to just store the file
        compression = zip.ZIP_DEFLATED
        print(f"HEIC.zip")
        zf = zip.ZipFile(f"HEIC.zip", mode="w")

        for file_to_write in filelist:
            try:
                print(f"{file_to_write}")
                # Add file to the zip file
                # first parameter file to zip, second filename in zip
                zf.write(f"{file_to_write}", file_to_write, compress_type=compression, compresslevel=0)
                os.remove(f"{file_to_write}")

            except FileNotFoundError as e:
                print(f' *** Exception occurred during zip process - {e}')
        logging.info(f"HEIC files zipped")
        zf.close()
            
def get_file():
    global file
    file = filedialog.askopenfile(title="Select a HEIC file")
    label.configure(text=f"Selected file: {file.name}")
    label.pack()
    

def get_directory():
    global dirs
    dirs = filedialog.askdirectory(title="Select directory")
    label.configure(text=f"Selected directory: {dirs}")
    label.pack()
    
def get_files():
    global file
    file = filedialog.askopenfiles(title="Select a HEIC file")
    label.configure(text=f"Selected files: {file.name}")
    label.pack()
    
def main():
    gui()
    logging.basicConfig(filename="latest.log", level=logging.INFO, filemode='w',format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    directorylist = folders(args)
    convert_rec(directorylist)

if __name__ == "__main__":
    main()