import os
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
from fileFilterer import backendFileProcessor

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

def uiBackendController():
    global retention_entry
    global retentionType
    global grouping_entry
    global groupingValue
    global varStorage
    global conversionRunning
    global runButton
    global files_upload
    global files_output
    global radio_one
    global radio_two
    global radio_three
    global radio_four
    global backendFileProcessorThread
    global terminationFlag

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
        
        if conversionRunning:
            if str(runButton["text"]) == "Convert":
                runButton.config(state=tk.DISABLED, text="            Converting...\nPress Again to Terminate")
                files_upload.config(state=tk.DISABLED)
                files_output.config(state=tk.DISABLED)
                radio_one.config(state=tk.DISABLED)
                radio_two.config(state=tk.DISABLED)
                radio_three.config(state=tk.DISABLED)
                radio_four.config(state=tk.DISABLED)
                retention_entry.config(state=tk.DISABLED)
                grouping_entry.config(state=tk.DISABLED)

            time.sleep(0.25)
            runButton.config(state=tk.NORMAL, command=stopThread)

            while not terminationFlag.is_set() and backendFileProcessorThread.is_alive():
                    runButton.config(text = '            Converting   \nPress Again to Terminate')
                    time.sleep(0.3)
                    runButton.config(text = '            Converting.  \nPress Again to Terminate')
                    time.sleep(0.15)
                    runButton.config(text = '            Converting.. \nPress Again to Terminate')
                    time.sleep(0.15)
                    runButton.config(text = '            Converting...\nPress Again to Terminate')
                    time.sleep(0.25)
            
            runButton.config(state=tk.DISABLED)

            while backendFileProcessorThread.is_alive():
                    runButton.config(text = 'Canceling   ')
                    time.sleep(0.3)
                    runButton.config(text = 'Canceling.  ')
                    time.sleep(0.15)
                    runButton.config(text = 'Canceling.. ')
                    time.sleep(0.15)
                    runButton.config(text = 'Canceling...')
                    time.sleep(0.25)
            conversionRunning = False
            terminationFlag.clear()

        else:
            if not str(runButton["text"]) == 'Convert':
                runButton.config(text="Convert", state=tk.NORMAL, command=convertFiles)
                files_upload.config(state=tk.NORMAL)
                files_output.config(state=tk.NORMAL)
                radio_one.config(state=tk.NORMAL)
                radio_two.config(state=tk.NORMAL)
                radio_three.config(state=tk.NORMAL)
                radio_four.config(state=tk.NORMAL)
                retention_entry.config(state=tk.NORMAL)
                grouping_entry.config(state=tk.NORMAL)

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
    global conversionRunning  
    global backendFileProcessorThread

    conversionRunning = True
    if groupingType.get():
        scalar = int(groupingValue.get())
        groups = None
    else:
        groups = int(groupingValue.get())
        scalar = None
    backendFileProcessorThread = threading.Thread(target=lambda:(backendFileProcessor(varStorage.inputs, varStorage.outputdir, retentionType.get(), 
        int(retentionValue.get()), terminationFlag, groups, scalar)))
    backendFileProcessorThread.daemon = True
    backendFileProcessorThread.start()

def stopThread():
    global terminationFlag
    terminationFlag.set()
#endregion

#region Window Settup
"""root => main window"""
root = tk.Tk()
root.title("Video to Image Dataset Converter")
root.resizable(False, False)

"""mainframe =>  tkinter frame that holds all the other components"""
mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.pack(expand=True, fill="none", anchor="center")

"""varStorage => Object that holds all the directories for the selected files"""
varStorage = Directories()

"""conversionRunning => Used to comunicate between the frontend and the backend that the conversion is currently running"""
conversionRunning = False
#endregion

#region Upload Video(s)
"""
Button to open the file prompt for the videos
"""

files_upload = tk.Button(mainframe, text='Select File(s)', command=select_files, width=13)
files_upload.grid(column=1, row=2, padx=10, pady=10)

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

radio_one = tk.Radiobutton(cullingsettings, text = "Percentage", variable = retentionType,
    value = True, font=("TkDefaultFont", 10))
radio_one.grid(column = 0, row = 0, sticky = (tk.W))

radio_two = tk.Radiobutton(cullingsettings, text = "Count", variable = retentionType,
    value = False, font=("TkDefaultFont", 10))
radio_two.grid(column = 1, row = 0, sticky = (tk.W))

retention_entry = tk.Entry(cullingsettings, textvariable = retentionValue, validate = "key", validatecommand = validatePercentcmd)
retention_entry.grid(column = 2, row = 0, sticky = (tk.W), padx = 10)

#True is scalar, false is group
groupingType = tk.BooleanVar(root, True) 
groupingValue = tk.StringVar(root, "6")

radio_three = tk.Radiobutton(cullingsettings, text = "Scalar", variable = groupingType, value = True, font=("TkDefaultFont", 10))
radio_three.grid(column=0, row=1, sticky=(tk.W))

radio_four = tk.Radiobutton(cullingsettings, text = "Groups", variable = groupingType, value = False, font=("TkDefaultFont", 10))
radio_four.grid(column=1, row=1, sticky=(tk.W))

grouping_entry = tk.Entry(cullingsettings, textvariable = groupingValue, validate="key", validatecommand=validateIntcmd)
grouping_entry.grid(column=2, row=1, sticky=(tk.W), padx=10)
#endregion

#region Process Button
runButton = ttk.Button(bottomButtons, text = 'Convert', command=convertFiles, width=30)
runButton.config(state=tk.DISABLED)
runButton.grid(column=1, row=0, sticky=(tk.NS))
#endregion
#endregion

thread = threading.Thread(target=uiBackendController)
thread.daemon = True
thread.start()

terminationFlag = threading.Event()

root.mainloop()