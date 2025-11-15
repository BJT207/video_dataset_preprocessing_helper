import os
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
import fileFilterer

#region Classes
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

        self.outputdir = outputdir

class AutoScrollbar(tk.Scrollbar):
    """
    A scrollbar that is automatically hidden when not needed.
    Only the grid geometry manager is supported in this example.
    """
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            # Hide scrollbar if content fits
            self.tk.call("grid", "remove", self)
        else:
            # Show scrollbar if content overflows
            self.grid()
        tk.Scrollbar.set(self, low, high)

class ScrollableFrame(ttk.Frame):
    """
    Foundational code for ScrollableFrame courtasy of https://blog.teclado.com/tkinter-scrollable-frames/
    """

    def __init__(self, container, *args, **kwargs):

        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)
        canvas.config(height=150, bg="#E6E6E6")
        scrollbarVert = AutoScrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        scrollbarHori = AutoScrollbar(self, orient="horizontal", command=canvas.xview)

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
    Foundational code for HorizontallyScrollableFrame courtasy of https://blog.teclado.com/tkinter-scrollable-frames/
    """

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        canvas.config(height=25, bg="#E6E6E6")
        self.scrollable_frame = ttk.Frame(canvas)
        scrollbarHori = AutoScrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbarHori.set)
        canvas.grid(sticky=(tk.NSEW))
        scrollbarHori.grid(column=0, row=1, sticky=(tk.W, tk.E))

    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            # Hide scrollbar if content fits
            self.tk.call("grid", "remove", self)
        else:
            # Show scrollbar if content overflows
            self.grid()
        tk.Scrollbar.set(self, low, high)
#endregion

#region Functions
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
    global inputFrame

    global fileList

    fileList.destroy()

    fileList = ttk.Frame(inputFrame.scrollable_frame)

    if file_path_tupple:        

        for path in file_path_tupple:

            ttk.Label(fileList, text=path).pack()

    fileList.grid(sticky=(tk.NE))
    
def setoutput_str(directory_path):
    """

    Sets the text in the GUI to display the output path
    """
    if directory_path:
        global outputFrame
        
        global outputList

        outputList.destroy()
        
        outputList = ttk.Frame(outputFrame.scrollable_frame)

        ttk.Label(outputList, text=directory_path).pack()

        outputList.grid(sticky=(tk.NE))

def validatePercent(P) -> bool:
    global retentionType
    if (P.isdigit() or P == '') and (len(P) <= 3 or (not retentionType.get())):
        return True
    return False

def validateInt(P) -> bool:
    if P.isdigit() or P =='':
        return True
    return False

def uiConstrainer():
    global retention_entry
    global retentionType
    global groupingValue
    global varStorage
    global runButton
    while True:
        if len(retention_entry.get()) >= 3 and retentionType.get():
            if retention_entry.get() == '000':
                retention_entry.delete(0,3)
            elif retention_entry.get()[0:2] == '00':
                retention_entry.delete(0,2)
            elif retention_entry.get()[0] == '0':
                retention_entry.delete(0,1)
            elif not retention_entry.get() == "100":
                retention_entry.delete(0,tk.END)
                retention_entry.insert(0, '100')
        elif len(retention_entry.get()) >= 2 and retentionType.get():
            if retention_entry.get()[0] == '00':
                retention_entry.delete(0,2)
        if retention_entry.get() and (not int(retention_entry.get()) == 0) and groupingValue.get() and varStorage.inputs and varStorage.outputdir:
            if str(runButton['state']) == 'disabled':
                runButton.config(state=tk.NORMAL)
        else:
            if str(runButton['state']) == "normal":
                runButton.config(state=tk.DISABLED)
        

        time.sleep(0.001)

def convertFiles():
    global varStorage
    global groupingType
    global groupingValue
    global retentionType
    global retentionValue

    fileFilterer.extract_frames(varStorage.inputs, varStorage.outputdir)
    if groupingType.get():
        scalar = int(groupingValue.get())
        groups = None
    else:
        groups = int(groupingValue.get())
        scalar = None
    print(int(retentionValue.get()))
    fileFilterer.filterImages(varStorage.outputdir,retentionType.get(), int(retentionValue.get()), groups, scalar)
#endregion

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

files_upload = tk.Button(mainframe, text='Select File(s)', command=select_files, width=13).grid(column=1, row=2, padx=10, pady=10)

"""
Scrollable sub-window to display all the uploaded videos
"""

inputFilesLable = tk.Label(mainframe, text=f"Input File(s):", font=("Arial", 12))

inputFilesLable.grid(column=0, row=1, pady=5, sticky=tk.W)


inputFrame = ScrollableFrame(mainframe)

inputFrame.grid(column=0, row=2)

fileList = ttk.Frame(inputFrame.scrollable_frame)

fileList.grid(sticky=(tk.NE))

#endregion

#region Choose Output Dir
"""Button to open the file prompt for the output Dir"""
files_output = tk.Button(mainframe, text='Select Output Dir', command=select_path)
files_output.grid(column=1,row=5, padx=10, pady=10)
files_output.config(height=1)
"""

Header that lables the output directory string
"""

outputDirLable = tk.Label(mainframe, text=f"Output Directory:", font=("Arial", 12))

outputDirLable.grid(column=0, row=4, pady=5, sticky=tk.W)

"""

text to display the output directory
"""

outputFrame = HorizontallyScrollableFrame(mainframe)

outputFrame.grid(column=0, row=5)

outputList = ttk.Frame(outputFrame.scrollable_frame)

outputList.grid(sticky=(tk.NE))
#endregion

#region Bottom Buttons
bottomButtons = ttk.Frame(mainframe)
bottomButtons.grid(column=0, row=6, columnspan=3, sticky=(tk.NSEW))
#region Culling Settings
cullingsettings = tk.Frame(bottomButtons)
cullingsettings.grid(column=0, row=0, sticky=(tk.NSEW))
#True is percentage, false is count
validatePercentcmd = root.register(validatePercent), '%P'
validateIntcmd = root.register(validateInt), '%P'
retentionType = tk.BooleanVar(root, True)
retentionValue = tk.StringVar(root, '50')

tk.Radiobutton(cullingsettings, text = "Percentage", variable = retentionType,
    value = True, font=("TkDefaultFont", 10)).grid(column = 0, row = 0, sticky = (tk.W))

tk.Radiobutton(cullingsettings, text = "Count", variable = retentionType,
    value = False, font=("TkDefaultFont", 10)).grid(column = 1, row = 0, sticky = (tk.W))

retention_entry = tk.Entry(cullingsettings, textvariable = retentionValue, validate = "key", validatecommand = validatePercentcmd)
retention_entry.grid(column = 2, row = 0, sticky = (tk.W), padx = 10)

#True is scalar, false is group
groupingType = tk.BooleanVar(root, True) 
groupingValue = tk.StringVar(root, "6")

tk.Radiobutton(cullingsettings, text = "Scalar", variable = groupingType, 

        value = True, font=("TkDefaultFont", 10)).grid(column=0, row=1, sticky=(tk.W))
tk.Radiobutton(cullingsettings, text = "Groups", variable = groupingType, 

        value = False, font=("TkDefaultFont", 10)).grid(column=1, row=1, sticky=(tk.W))

tk.Entry(cullingsettings, textvariable = groupingValue, validate="key", validatecommand=validateIntcmd).grid(column=2, row=1, sticky=(tk.W), padx=10)
#endregion

#region Process Button
runButton = ttk.Button(bottomButtons, text = 'Convert', command=convertFiles, width=30)
runButton.config(state=tk.DISABLED)
runButton.grid(column=1, row=0, sticky=(tk.NS))
#endregion


thread = threading.Thread(target=uiConstrainer)
thread.daemon = True
thread.start()
#endregion

root.mainloop()