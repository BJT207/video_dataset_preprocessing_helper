import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from dataclasses import dataclass

class Directories():

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
    Code courtasy of https://blog.teclado.com/tkinter-scrollable-frames/
    """
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def select_files():    
    '''
    This function opens a file dialoge for the user to select files
    for the data processing
    '''
    
    file_paths = filedialog.askopenfilenames(filetypes=[("Videos","*.mov"),("Videos","*.mp4")])
    setinput_str(file_paths)
    global varStorage
    varStorage.setInputs(file_paths)

def select_path():
    '''
    This function asks user to select a path
    '''
    file_path = filedialog.askdirectory()
    setoutput_str(file_path)
    global varStorage
    varStorage.setOutputDir(file_path)

def setinput_str(file_path_tupple):
    if file_path_tupple:
        global inputFrame
        global fileList
        fileList.destroy()
        fileList = ttk.Frame(inputFrame.scrollable_frame)
        
        for path in file_path_tupple:
            ttk.Label(fileList, text=path).pack()
        
        fileList.pack(anchor='center')
    
def setoutput_str(file_path):
    global outputDirLable
    outputDirLable.config(text=f"Output Directory: {os.path.basename(file_path)}")

def convertFiles():
    pass

#region Window Settup
root = tk.Tk()
root.title("Video to Image Dataset Converter")
root.resizable(False, False)
mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.pack(expand=True, fill="none", anchor="center")
varStorage = Directories()
#endregion

files_upload = tk.Button(mainframe, text='Select File(s)', command=select_files).grid(column=2, row=1, padx=10, pady=10)
inputFrame = ScrollableFrame(mainframe)
inputFrame.grid(column=1, row=1)
fileList = ttk.Frame(inputFrame.scrollable_frame)
fileList.pack(anchor='ne')
#label = tk.Label(mainframe, text=f"Input Files:", font=("Arial", 12))
#label.grid(column=2, row=2, padx=10, pady=10)

files_output = tk.Button(mainframe, text='Select Output Dir', command=select_path).grid(column=2,row=4, padx=10, pady=10, rowspan=2, sticky=(tk.N, tk.S))
outputDirLable = tk.Label(mainframe, text=f"Output Directory:", font=("Arial", 12))
outputDirLable.grid(column=1, row=4, padx=10, pady=5)

outputDirtext = tk.Label(mainframe, text=f" ", font=("Arial", 8))
outputDirtext.grid(column=1, row=5, padx=10)

#retentionsettings = tk.Frame(mainframe, )

#True is percentage, false is count
retentionType = tk.BooleanVar(root, True) 

values = {"Percentage" : True, 
    "Count" : False, 
    }

for (text, value) in values.items(): 
    tk.Radiobutton(root, text = text, variable = retentionType, 
        value = value).pack(side = tk.LEFT, ipadx = 5)


root.mainloop()