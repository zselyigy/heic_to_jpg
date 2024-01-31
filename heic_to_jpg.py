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
    global recc, delc, zipc
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
    fsb = ctk.CTkButton(master=root, text="Choose files", command=get_files).pack()
    convfb = ctk.CTkButton(master=root, text="Convert files/directory", command=conversion).pack()
    recc = ctk.CTkCheckBox(master=root, text="Run in all subdirectories?", onvalue=True, offvalue=False)
    delc = ctk.CTkCheckBox(master=root, text="Delete processed HEIC files?", onvalue=True, offvalue=False)
    zipc = ctk.CTkCheckBox(master=root, text="Zip processed HEIC files?", onvalue=True, offvalue=False)
    recc.pack()
    delc.pack()
    zipc.pack()
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

            if zipc.get() == 1:
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
                    except FileNotFoundError as e:
                        print(f' *** Exception occurred during zip process - {e}')
                    logging.info(f"{directory} HEIC files zipped")
                    zf.close()
            if delc.get() == 1:
                for file_to_write in files:
                    os.remove(f"{directory}/{file_to_write}")
                

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

        if zipc.get() == 1:
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

                except FileNotFoundError as e:
                    print(f' *** Exception occurred during zip process - {e}')
            logging.info(f"{directory} HEIC files zipped")
            zf.close()
        if delc.get() == 1:
                for file_to_write in files:
                    os.remove(f"{directory}/{file_to_write}")
def convert_f(file):
    command = rf'.\.venv\Scripts\heif-convert.exe -o {file[:-5]} -p "{file}" -q 95 "{file}"'
    #
    try:
        subprocess.run(command, shell=True, check=True)
        logging.info(f"{file} ---> {file[:-5]}.jpg)")
    except:
        print(f"Error converting {file}")
    if delc.get() == 1:
        os.remove(f"{file}")

def convert_fs(filelist):
    for filename in filelist:
        command = rf'.\.venv\Scripts\heif-convert.exe -o {filename[:-5]} -p "{os.path.dirname(filename)}" -q 95 "{filename}"'
        try:
            subprocess.run(command, shell=True, check=True)
            logging.info(f"{os.path.basename(filename)} ---> {os.path.basename(filename)}.jpg")
        except:
            print(f"Error converting {filename}")
    if zipc.get() == 1:
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
                zf.write(f"{os.path.basename(file_to_write)}", os.path.basename(file_to_write), compress_type=compression, compresslevel=0)

            except FileNotFoundError as e:
                print(f' *** Exception occurred during zip process - {e}')
        logging.info(f"HEIC files zipped")
        zf.close()
    for file_obj in file:
        file_obj.close()
    if delc.get() == 1:
        for file_to_write in filelist:
            os.remove(f"{file_to_write}")
 

def conversion():
    if dirs == "":
        if type(file) == list:
            convert_fs([f.name for f in file])
        else:
            convert_f(file.name)
    else:
        if recc.get() == 1:
            convert_rec(folders())
        else:
            convert(dirs)
        
def get_file():
    global file
    global dirs
    dirs = ""
    file = filedialog.askopenfile(title="Select a HEIC file", filetypes=[("HEIC file","*.HEIC")])
    label.configure(text=f"Selected file: {file.name}")
    label.pack()
    

def get_directory():
    global dirs
    global file
    file = ""
    dirs = filedialog.askdirectory(title="Select directory")
    label.configure(text=f"Selected directory: {dirs}")
    label.pack()
    
def get_files():
    global file
    global dirs
    dirs = ""
    file = filedialog.askopenfiles(title="Select a HEIC file", filetypes=[("HEIC file","*.HEIC")])
    label.configure(text=f"Selected files: {[f.name for f in file]}")
    label.pack()
    
def main():
    logging.basicConfig(filename="latest.log", level=logging.INFO, filemode='w',format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    gui()
    

if __name__ == "__main__":
    main()