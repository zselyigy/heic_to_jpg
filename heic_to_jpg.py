import os
import subprocess
import sys
import zipfile as zip
import logging
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog

# TODO Create executable, https://customtkinter.tomschimansky.com/documentation/packaging

def gui():
    """
    Function to create a Graphical User Interface (GUI) for HEIC to jpg converter.

    Global Variables:
    - label: Tkinter label to display file or directory path.
    - quall: Tkinter label to display quality setting.
    - recc: Tkinter checkbox for running in all subdirectories.
    - delc: Tkinter checkbox for deleting processed HEIC files.
    - zipc: Tkinter checkbox for zipping processed HEIC files.
    - modesw: Tkinter switch for toggling dark mode.
    - quals: Tkinter slider to adjust quality of converted images.
    - q: Default quality value set to 95.

    Returns:
    - None

    Creates a GUI window using CTk library with buttons, checkboxes, switch, slider, and labels for various functionalities.
    """
    global label, quall
    global recc, delc, zipc
    global modesw
    global quals
    global q
    global root
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
    convfb = ctk.CTkButton(master=root, text="Convert files/directory", command=conversion, height=100, font=("Arial", 20), fg_color='blue4')
    recc = ctk.CTkCheckBox(master=root, text="Run in all subdirectories?", onvalue=True, offvalue=False,font=("Arial", 20))
    delc = ctk.CTkCheckBox(master=root, text="Delete processed HEIC files?", onvalue=True, offvalue=False,font=("Arial", 20))
    zipc = ctk.CTkCheckBox(master=root, text="Zip processed HEIC files?", onvalue=True, offvalue=False,font=("Arial", 20))
    modesw = ctk.CTkSwitch(master=root, text="Dark mode", onvalue=True, offvalue=False, command=change_mode,font=("Arial", 20))
    quals = ctk.CTkSlider(master=root, from_=1, to=100, command=quality, progress_color="#1f538d", number_of_steps=99, button_color="#102a47")

    # file/directory buttons in the first line
    fb.grid(row=1, column=2, sticky="we")
    fsb.grid(row=1, column=4, sticky="we")
    db.grid(row=1, column=6, sticky="we")

    # dark mode selector in the left bottom corner
    modesw.grid(row=9, column=0, sticky="we")

    # quality selection and options in the middle column
    # quality selection
    modesw.select()
    quals.set(95)
    label = ctk.CTkLabel(root, width=root.winfo_width(), text="File or directory path will appear here.", corner_radius=5, anchor="center", font=("Arial", 20), wraplength=340)
    quall = ctk.CTkLabel(root, text=f"Quality: {q}", corner_radius=5, font=("Arial", 20))
    quall.grid(row=2, column=4, sticky="we")
    label.grid(row=0, column=4, sticky= "we")
    # options
    quals.grid(row=3, column=4, sticky="we")
    recc.grid(row=4, column=4, sticky="we")
    delc.grid(row=5, column=4, sticky="we")
    zipc.grid(row=6, column=4, sticky="we")
    
    # convert button in the middle bottom of the screen
    convfb.grid(row=8, column=4, sticky="we")
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    
def on_closing():
    """
    Function to handle the closing event of the application window.

    Returns:
    - None

    Displays a confirmation dialog asking if the user wants to quit.
    If the user confirms, it destroys the root window, closing the application.
    """
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy() 
    
def change_mode():
    """
    Function to change the appearance mode of the GUI based on the state of the mode switch.

    Returns:
    - None

    If the mode switch is toggled to dark mode, it sets the appearance mode to "dark" and updates the colors of the quality slider accordingly.
    If the mode switch is toggled to light mode, it sets the appearance mode to "light" and updates the colors of the quality slider accordingly.
    """
    if modesw.get():
        ctk.set_appearance_mode("dark")
        quals.configure(progress_color="#1f538d", button_color="#102a47")
    else:
        ctk.set_appearance_mode("light")
        quals.configure(progress_color="#4c75a4", button_color = "#1f538d")

def quality(new):
    """
    Function to update the quality value based on the slider position.

    Args:
    - new: New value selected on the slider.

    Global Variables:
    - q: Quality value.

    Returns:
    - None

    Updates the global quality value based on the new slider position, updates the quality label to display the new value, and prints the new value.
    """
    global q
    q = int(new)
    quall.configure(text=f"Quality: {q}")
    print(q)

def folders():
    """
    Function to recursively list all directories within a given directory.

    Returns:
    - directorylist: List of all directories within the specified directory.

    Uses a breadth-first search algorithm to traverse all directories within the specified directory,
    replaces backslashes with forward slashes in the directory path, and returns a list of all directories.
    """
    i = 0
    directory = dirs.replace('\\', '/')
    directorylist = [directory]
    while i < len(directorylist):
        print(i)
        dir = [f"{directorylist[i]}/{f}" for f in os.listdir(directorylist[i]) if os.path.isdir(f"{directorylist[i]}/{f}")]
        for darab in dir:
            directorylist.append(dir)
        i += 1
    return directorylist
    
def convert_rec(directorylist):
    """
    Function to recursively convert HEIC/HEIF files to JPG within a list of directories.

    Args:
    - directorylist: List of directories to search for HEIC/HEIF files.

    Returns:
    - None

    Iterates over each directory in the directory list, identifies HEIC/HEIF files, and converts them to JPG format.
    Additionally, it provides options to zip processed HEIC files and delete them after conversion.

    """
    for directory in directorylist:
        files = [f for f in os.listdir(directory) if f.lower().endswith('.heic') or f.lower().endswith('.heif')]
        if len(files) != 0:
            for filename in files:
                command = rf'.\.venv\Scripts\heif-convert.exe -o "{filename[:-5]}" -p "{directory}" -q {q} "{directory}/{filename}"'
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
    """
    Function to convert HEIC/HEIF files to JPG within a specified directory.

    Args:
    - directory: Directory path to search for HEIC/HEIF files.

    Returns:
    - None

    Identifies HEIC/HEIF files within the specified directory and converts them to JPG format.
    Additionally, it provides options to zip processed HEIC files and delete them after conversion.
    """
    files = [f for f in os.listdir(directory) if f.lower().endswith('.heic') or f.lower().endswith('.heif')]
    if len(files) != 0:
        for filename in files:
            command = rf'.\.venv\Scripts\heif-convert.exe -o "{filename[:-5]}" -p "{directory}" -q {q} "{directory}/{filename}"'
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
                    os.remove(f"'{directory}/{file_to_write}'")
def convert_f(file):
    """
    Function to convert a single HEIC/HEIF file to JPG.

    Args:
    - file: Path of the HEIC/HEIF file to be converted.

    Returns:
    - None

    Converts the specified HEIC/HEIF file to JPG format.
    Additionally, it provides an option to delete the original file after conversion.
    """
    command = rf'.\.venv\Scripts\heif-convert.exe -o "{file[:-5]}" -p "{file}" -q {q} "{file}"'
    #
    try:
        subprocess.run(command, shell=True, check=True)
        logging.info(f"{file} ---> {file[:-5]}.jpg)")
    except:
        print(f"Error converting {file}")
    if delc.get() == 1:
        os.remove(f"{file}")

def convert_fs(filelist):
    """
    Function to convert a list of HEIC/HEIF files to JPG.

    Args:
    - filelist: List of paths of HEIC/HEIF files to be converted.

    Returns:
    - None

    Converts each HEIC/HEIF file in the list to JPG format.
    Additionally, it provides options to zip processed HEIC files and delete them after conversion.
    """
    for filename in filelist:
        command = rf'.\.venv\Scripts\heif-convert.exe -o "{filename[:-5]}" -p "{os.path.dirname(filename)}" -q {q} "{filename}"'
        print(command)
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
# TODO fix the zipping error when space containing file names are used
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
    """
    Function to initiate the conversion process based on user input.

    Returns:
    - None

    If no directory is specified, it checks if the input is a list of files or a single file and initiates the conversion accordingly.
    If a directory is specified and the recursive checkbox is selected, it initiates recursive conversion within all subdirectories.
    Otherwise, it initiates conversion within the specified directory.
    """
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
    """
    Function to open a file dialog for selecting a single HEIC file.

    Returns:
    - None

    Opens a file dialog window to select a HEIC file.
    Updates the global 'file' variable with the selected file object.
    If a file is selected, it updates the label to display the selected file path.
    """
    global file
    global dirs
    dirs = ""
    file = filedialog.askopenfile(title="Select a HEIC file", filetypes=[("HEIC file","*.HEIC")])
    if file != "":
        label.configure(text=f"Selected file: {file.name}")
        label.grid(row=0, column=4, sticky= "we")
    

def get_directory():
    """
    Function to open a directory dialog for selecting a directory.

    Returns:
    - None

    Opens a directory dialog window to select a directory.
    Updates the global 'dirs' variable with the selected directory path.
    If a directory is selected, it updates the label to display the selected directory path.
    """
    global dirs
    global file
    file = ""
    dirs = filedialog.askdirectory(title="Select directory")
    if dirs != "":
        label.configure(text=f"Selected directory: {dirs}")
        label.grid(row=0, column=4, sticky= "we")
    
def get_files():
    """
    Function to open a file dialog for selecting multiple HEIC files.

    Returns:
    - None

    Opens a file dialog window to select multiple HEIC files.
    Updates the global 'file' variable with a list of selected file objects.
    If files are selected, it updates the label to display the selected file paths.
    """
    global file
    global dirs
    dirs = ""
    file = filedialog.askopenfiles(title="Select HEIC files", filetypes=[("HEIC file","*.HEIC")])
    if len(file) != 0:
        label.configure(text=f"Selected files: {[f.name for f in file]}")
        label.grid(row=0, column=4, sticky= "we")
    
def main():
    
    """
    Main function to start the HEIC to JPG converter application.

    Returns:
    - None

    Configures logging settings, initializes the GUI, and starts the main event loop.
    """
    logging.basicConfig(filename="latest.log", level=logging.INFO, filemode='w',format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    gui()
    

if __name__ == "__main__":
    main()