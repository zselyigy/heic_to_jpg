import os
import subprocess
import sys
import zipfile as zip
import logging
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog

def gui():
    global label, quall
    global recc, delc, zipc
    global modesw
    global quals
    global q
    q = 95
    
    #Set the theme and color options
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    #Create root object
    root = ctk.CTk()
    #Set GUI title
    root.title("HEIC to jpg converter")
    #Set GUI size to zoomed
    root.after(1, lambda: root.state("zoomed"))
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)
    root.columnconfigure(4, weight=1)
    root.columnconfigure(5, weight=1)
    root.columnconfigure(6, weight=1)
    root.columnconfigure(7, weight=1)
    root.columnconfigure(8, weight=1)
    root.columnconfigure(9, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    root.rowconfigure(4, weight=1)
    root.rowconfigure(5, weight=1)
    root.rowconfigure(6, weight=1)
    root.rowconfigure(7, weight=1)
    root.rowconfigure(8, weight=1)
    root.rowconfigure(9, weight=1)

    fb = ctk.CTkButton(master=root, text="Choose file", command=get_file, height=100, font=("Arial", 20))
    db = ctk.CTkButton(master=root, text="Choose directory", command=get_directory, height=100, font=("Arial", 20))
    fsb = ctk.CTkButton(master=root, text="Choose files", command=get_files, height=100, font=("Arial", 20))
    convfb = ctk.CTkButton(master=root, text="Convert files/directory", command=conversion, height=100, font=("Arial", 20))
    recc = ctk.CTkCheckBox(master=root, text="Run in all subdirectories?", onvalue=True, offvalue=False,font=("Arial", 20))
    delc = ctk.CTkCheckBox(master=root, text="Delete processed HEIC files?", onvalue=True, offvalue=False,font=("Arial", 20))
    zipc = ctk.CTkCheckBox(master=root, text="Zip processed HEIC files?", onvalue=True, offvalue=False,font=("Arial", 20))
    modesw = ctk.CTkSwitch(master=root, text="Dark mode", onvalue=True, offvalue=False, command=change_mode,font=("Arial", 20))
    quals = ctk.CTkSlider(master=root, from_=1, to=100, command=quality, progress_color="#1f538d", number_of_steps=99, button_color="#102a47")
    quals.grid(row=3, column=4, sticky="we")
    modesw.grid(row=9, column=0, sticky="we")
    recc.grid(row=4, column=4, sticky="we")
    delc.grid(row=5, column=4, sticky="we")
    zipc.grid(row=6, column=4, sticky="we")
    fb.grid(row=1, column=0, sticky="we")
    fsb.grid(row=1, column=2, sticky="we")
    db.grid(row=1, column=6, sticky="we")
    convfb.grid(row=1, column=4, sticky="we")
    modesw.select()
    quals.set(95)
    label = ctk.CTkLabel(root, width=root.winfo_width(), text="File or directory path will appear here.", corner_radius=5, anchor="center", font=("Arial", 20))
    quall = ctk.CTkLabel(root, text=f"Quality: {q}", corner_radius=5, font=("Arial", 20))
    quall.grid(row=2, column=4, sticky="we")
    label.grid(row=0, column=4, sticky= "we")
    root.mainloop()
    
def change_mode():
    if modesw.get():
        ctk.set_appearance_mode("dark")
        quals.configure(progress_color="#1f538d", button_color="#102a47")
    else:
        ctk.set_appearance_mode("light")
        quals.configure(progress_color="#4c75a4", button_color = "#1f538d")

def quality(new):
    global q
    q = int(new)
    quall.configure(text=f"Quality: {q}")
    print(q)

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
                command = rf'.\.venv\Scripts\heif-convert.exe -o {filename[:-5]} -p "{directory}" -q {q} "{directory}/{filename}"'
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
            command = rf'.\.venv\Scripts\heif-convert.exe -o {filename[:-5]} -p "{directory}" -q {q} "{directory}/{filename}"'
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
    command = rf'.\.venv\Scripts\heif-convert.exe -o {file[:-5]} -p "{file}" -q {q} "{file}"'
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
        command = rf'.\.venv\Scripts\heif-convert.exe -o {filename[:-5]} -p "{os.path.dirname(filename)}" -q {q} "{filename}"'
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
    if file != "":
        label.configure(text=f"Selected file: {file.name}")
        label.grid(row=0, column=4, sticky= "we")
    

def get_directory():
    global dirs
    global file
    file = ""
    dirs = filedialog.askdirectory(title="Select directory")
    if dirs != "":
        label.configure(text=f"Selected directory: {dirs}")
        label.grid(row=0, column=4, sticky= "we")
    
def get_files():
    global file
    global dirs
    dirs = ""
    file = filedialog.askopenfiles(title="Select HEIC files", filetypes=[("HEIC file","*.HEIC")])
    if len(file) != 0:
        label.configure(text=f"Selected files: {[f.name for f in file]}")
        label.grid(row=0, column=4, sticky= "we")
    
def main():
    logging.basicConfig(filename="latest.log", level=logging.INFO, filemode='w',format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    gui()
    

if __name__ == "__main__":
    main()