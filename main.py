import os

import tkinter as tk

from tkinter import filedialog

from tkinter import ttk
from dataclasses import dataclass


class Directories():
    """

    Holds the paths of the user selected files and or directories
    """

    def __init__(self):

        self.inputs = []

        self.outputdir = ''
    

    def setInputs(self, files:tuple[str]):
        self.inputs.clear()

        for file in files:
            self.inputs.append(file)
    

    def setOutputDir(self, outputdir:str):

        self.outputDir = outputdir
        


class ScrollableFrame(ttk.Frame):
    """
    Foundational code for ScrollableFrame courtasy of https://blog.teclado.com/tkinter-scrollable-frames/
    """

    def __init__(self, container, *args, **kwargs):

        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)

        scrollbarVert = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        scrollbarHori = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)

        self.scrollable_frame.bind(

            "<Configure>",

            lambda e: canvas.configure(

                scrollregion=canvas.bbox("all")
            )
        )

        

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")


        canvas.configure(yscrollcommand=scrollbarVert.set)
        canvas.configure(xscrollcommand=scrollbarHori.set)


        canvas.grid(sticky=(tk.NSEW))

        scrollbarVert.grid(column=1, row=0, sticky=(tk.N, tk.S))
        scrollbarHori.grid(column=0, row=1, sticky=(tk.W, tk.E))

class HorizontallyScrollableFrame(ttk.Frame):
    """
    Foundational code for ScrollableFrame courtasy of https://blog.teclado.com/tkinter-scrollable-frames/
    """

    def __init__(self, container, *args, **kwargs):

        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)

        scrollbarVert = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        scrollbarHori = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)

        self.scrollable_frame.bind(

            "<Configure>",

            lambda e: canvas.configure(

                scrollregion=canvas.bbox("all")
            )
        )

        

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")


        canvas.configure(yscrollcommand=scrollbarVert.set)
        canvas.configure(xscrollcommand=scrollbarHori.set)


        canvas.grid(sticky=(tk.NSEW))

        scrollbarVert.grid(column=1, row=0, sticky=(tk.N, tk.S))
        scrollbarHori.grid(column=0, row=1, sticky=(tk.W, tk.E))
    
def select_files():    

    '''

    This function opens a file dialoge for the user to select videos

    for the data processing and then stores it in the Directories Class

    '''
    

    file_paths = filedialog.askopenfilenames(filetypes=[("Videos","*.mov"),("Videos","*.mp4")])

    setinput_str(file_paths)

    global varStorage

    varStorage.setInputs(file_paths)


def select_path():

    '''

    This function asks the user to select a path for the photos

    to be output to and then stores it in the Directories Class

    '''

    file_path = filedialog.askdirectory()

    setoutput_str(file_path)

    global varStorage

    varStorage.setOutputDir(file_path)


def setinput_str(file_path_tupple):
    """

    Controls the paths displayed in the GUI
    

    TODO: add a button next to each file that can be used to 

    remove it from the list without having to open the files prompt again
    """

    if file_path_tupple:

        global inputFrame

        global fileList

        fileList.destroy()

        fileList = ttk.Frame(inputFrame.scrollable_frame)
        

        for path in file_path_tupple:

            ttk.Label(fileList, text=path).pack()
        

        fileList.grid(sticky=(tk.NE))
    

def setoutput_str(file_path):
    """

    Sets the text in the GUI to display the output path
    """

    global outputDirLable

    outputDirLable.config(text=f"Output Directory: {os.path.basename(file_path)}")


def convertFiles():
    pass


#region Window Settup
"""

root => main window
"""

root = tk.Tk()

root.title("Video to Image Dataset Converter")

root.resizable(False, False)
"""

mainframe =>  tkinter frame that holds all the other components
"""

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))

mainframe.pack(expand=True, fill="none", anchor="center")
"""

varStorage => Object that holds all the directories for the selected files
"""

varStorage = Directories()

#endregion


#region Upload Video(s)
"""

Button to open the file prompt for the videos
"""

files_upload = tk.Button(mainframe, text='Select File(s)', command=select_files).grid(column=2, row=1, padx=10, pady=10)

"""

Scrollable sub-window to display all the uploaded videos
"""

inputFrame = ScrollableFrame(mainframe)

inputFrame.grid(column=1, row=1)

fileList = ttk.Frame(inputFrame.scrollable_frame)

fileList.grid(sticky=(tk.NE))

#endregion


#region Choose Output Dir
"""

Button to open the file prompt for the output Dir
"""

files_output = tk.Button(mainframe, text='Select Output Dir', command=select_path).grid(column=2,row=4, padx=10, pady=10, rowspan=2, sticky=(tk.N, tk.S))

"""

Header that lables the output directory string
"""

outputDirLable = tk.Label(mainframe, text=f"Output Directory:", font=("Arial", 12))

outputDirLable.grid(column=1, row=4, padx=10, pady=5, sticky=tk.W)

"""

text to display the output directory
"""

outputDirtext = tk.Label(mainframe, text=f" ", font=("Arial", 8))

outputDirtext.grid(column=1, row=5, padx=10)

#endregion


cullingsettings = tk.Frame(mainframe)

cullingsettings.grid(column=1, row=6, sticky=(tk.W))


#True is percentage, false is count

retentionType = tk.BooleanVar(root, True) 


tk.Radiobutton(cullingsettings, text = "Percentage", variable = retentionType, 

        value = True).grid(column=0, row=0, sticky=(tk.W))

tk.Radiobutton(cullingsettings, text = "Count", variable = retentionType, 

        value = False).grid(column=1, row=0, sticky=(tk.W))



#True is scalar, false is group

groupingType = tk.BooleanVar(root, True) 


groupingvalues = {"Scalar" : True, 

    "Groups" : False, 

    }


tk.Radiobutton(cullingsettings, text = "Scalar", variable = groupingType, 

        value = True).grid(column=0, row=1, sticky=(tk.W))

tk.Radiobutton(cullingsettings, text = "Groups", variable = groupingType, 

        value = False).grid(column=1, row=1, sticky=(tk.W))

root.mainloop()