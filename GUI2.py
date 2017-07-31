from tkinter import * 
from tkinter import ttk, filedialog, messagebox
#Tk, Label, Button, filedialog, messagebox, Canvas
#import matplotlib as mp
from os import listdir
from PIL import ImageTk, Image
import random

class GUI:
    def __init__(self, master):

        # Variables
        self.imageNameListbox = StringVar()
        self.imageResultListbox = StringVar()
        self.entryFolderName = StringVar()
        self.entryResultName = StringVar()
        self.singleImageResult = StringVar()
        self.totalImgNumber = 0
        self.curImgNumber = 0
        self.imageList = []
        self.resultList = []
        self.imageResultList = []
        self.imageFolderDir = ''
        

        self.img = None
        self.img_label = None
        self.defaultImgDir = r"C:/Users/IceFox/AI_core/Project/GUI/TestGUI01/40X/"
        self.ImgDir = ""

        # GUI
        self.master = master
        self.master.resizable(width = FALSE, height = FALSE)
        self.master.title("Cancer Classifier")

        # Frame
        self.frame = ttk.Frame(self.master, padding=(5, 5, 12, 0))
        self.frame.pack(fill = BOTH, expand = 1)
        
        for row in range(9):
            self.frame.grid_rowconfigure(row, minsize = 15)
        for column in range(6):
            self.frame.grid_columnconfigure(column, minsize = 15)
        self.frame.grid_columnconfigure(0, minsize = 200)
        self.frame.grid_columnconfigure(1, minsize = 5)

        # Title (maybe not needed?)
        self.labelTitle = Label(self.frame, text= "Cancer Classifier v1.0")
        self.labelTitle.grid(row = 0, column = 3, sticky = W)

        # dir entry & load
        self.labelFolder = Label(self.frame, text = "Image Folder Dir:")
        self.labelFolder.grid(row = 1, column = 0, sticky = E)
        self.entryFolder = Entry(self.frame, textvariable = self.entryFolderName)
        self.entryFolder.grid(row = 1, column = 1, columnspan = 4, sticky = W+E)
        self.btnFolder = Button(self.frame, text = "Load", command = self.LoadFromDir)
        self.btnFolder.grid(row = 1, column = 5, sticky = W)
        #self.btnFolder = Button(self.frame, text = "DebugLoad", command = self.LoadDir)
        #self.btnFolder.grid(row = 1, column = 6, sticky = W)

        self.labelResult = Label(self.frame, text = "Classification Result Dir:")
        self.labelResult.grid(row = 2, column = 0, sticky = E)
        self.entryResultDir = Entry(self.frame, textvariable = self.entryResultName)
        self.entryResultDir.grid(row = 2, column = 1, columnspan = 4,sticky = W+E)
        self.btnFolder = Button(self.frame, text = "Save", command = self.LoadDir)
        self.btnFolder.grid(row = 2, column = 5, sticky = W)

        # main panel for labeling
        self.labelFolder = Label(self.frame, text = "Image in the folder:")
        self.labelFolder.grid(row = 3, column = 0, sticky = S)
        self.imgNameListStringVar = StringVar(value = self.imageList)
        self.imageListbox = Listbox(self.frame, listvariable = self.imgNameListStringVar, height=5)
        self.imageListbox.grid(row = 4, column = 0, rowspan = 5 , sticky=(N,S,E,W))
        self.imageNameLabel = Label(self.frame, textvariable = self.imageNameListbox)
        self.imageNameLabel.grid(row = 3, column = 3, columnspan = 3, sticky = W)

        # Result panel 
        self.labelResultList = Label(self.frame, text = "Results:")
        self.labelResultList.grid(row = 3, column = 1, sticky = S)
        self.imageResultListStringVar = StringVar(value = self.resultList)
        self.imageResultListbox = Listbox(self.frame, listvariable = self.imageResultListStringVar, height = 5, width = 8)
        self.imageResultListbox.grid(row = 4, column = 1, rowspan = 5 , sticky=(N,S,E,W))


        self.labelImageResult = Label(self.frame, textvariable = self.singleImageResult,  fg = "blue", bg = "yellow", font = "Verdana 10 bold")
        self.labelImageResult.grid(row = 4, column = 5, sticky = E)

        #self.imageListbox.bind('<<ListboxSelect>>', self.DisplaySelectedImageName)
        self.imageListbox.bind('<Double-1>',  self.ListboxSelected)

        # canvas
        self.canvas = Canvas(self.frame, background='white')
        self.canvas.grid(row = 5, column = 3, rowspan = 2, columnspan = 3)


        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 7, column = 2, columnspan = 5, sticky = W+E)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)


        self.classifyPanel = Frame(self.frame)
        self.classifyPanel.grid(row = 9, column = 2, columnspan = 5, sticky = W+E)
        self.classifyBtn = Button(self.classifyPanel, text='Run Classification', width = 25, command = self.ClassifySingleImage)
        self.classifyBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.classifyAllBtn = Button(self.classifyPanel, text='Run Classification on All', width = 30, command = self.ClassifyAllImages)
        self.classifyAllBtn.pack(side = LEFT, padx = 5, pady = 3)
        #self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        #self.progLabel.pack(side = LEFT, padx = 5)
        #self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        #self.tmpLabel.pack(side = LEFT, padx = 5)
        #self.idxEntry = Entry(self.ctrPanel, width = 5)
        #self.idxEntry.pack(side = LEFT)
        #self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        #self.goBtn.pack(side = LEFT)

    def prevImage(self, event = None):
        #print("previous image")
        if self.curImgNumber > 0:
            self.curImgNumber -= 1
            self.imageListbox.see(self.curImgNumber)
            self.LoadImage(self.imageList[self.curImgNumber])

    def nextImage(self, event = None):
        #print("next image")
        if self.curImgNumber < self.totalImgNumber - 1:
           self.curImgNumber += 1
           self.imageListbox.see(self.curImgNumber)
           self.LoadImage(self.imageList[self.curImgNumber])

    def gotoImage(self):
        #print("goto image")
        idx = int(self.idxEntry.get()) - 1
        if 0 <= idx and idx < self.totalImgNumber :
            self.curImgNumber = idx
            self.LoadImage(self.imageList[self.curImgNumber])

    def ClassifySingleImage(self):
        print("classify single image")

        #messagebox.showinfo("Results", "I don't know")


    def ClassifyAllImages(self):
        #print("classify all images")
        if (self.totalImgNumber!= 0):
            self.resultList = []
            for i in range(self.totalImgNumber):
                name = self.imageList[i] 
                if name != "":
                    if self.ImgDir != "":
                        fileDirectory = self.ImgDir + name
                    else:
                        fileDirectory = self.defaultImgDir + name
                    result = "B" if self.Classify(fileDirectory) == 0 else "M"
                    self.resultList.append(result)
            self.imageResultListStringVar.set(value = self.resultList)
            self.LoadImage(self.imageList[self.curImgNumber])
        else:
            messagebox.showinfo("Error", "No images in the selected directory")


    def Classify(self, fileDirectory):
        return random.randint(0, 1)


    def ImportFolder(self):
        self.imageFolderDir = listdir(self.defaultImgDir)
        self.imageList = []
        for image in self.imageFolderDir:
            #print(image)
            self.imageList.append(image)
        self.total = len(self.imageList)

    def DebugIncreaseList(self):
        print("increase")
        #print(self.imageList)

    def ListboxSelected(self, event = None):
        idxs = self.imageListbox.curselection()
        if len(idxs) == 1:
            idx = int(idxs[0])
            self.curImgNumber = idx
            self.imageListbox.see(idx)
            name = self.imageList[idx] 
            self.LoadImage(name)       


    def LoadImage(self, name):
        if name != "":
            self.progLabel.config(text = "%04d/%04d" %(self.curImgNumber + 1, self.totalImgNumber))
            self.imageNameListbox.set("Image Loaded: %s" % (name))

            if self.ImgDir != "":
                filename = self.ImgDir + name
            else:
                filename = self.defaultImgDir + name
            self.img = ImageTk.PhotoImage(Image.open(filename).resize((385, 253), Image.ANTIALIAS))
            self.canvas.config(width = 385, height = 253)
            self.canvas.create_image(0, 0, image = self.img, anchor=NW)
            if self.resultList[self.curImgNumber] == "":
                self.singleImageResult.set(value = "Not classified yet")
            elif self.resultList[self.curImgNumber] == "B" :
                self.singleImageResult.set(value = "Benign tumor")
            elif self.resultList[self.curImgNumber] == "M" :
                self.singleImageResult.set(value = "Malignant tumor")
            

    def DebugProduceFakeResult(self):
        if (self.totalImgNumber != 0):
            print(self.ResultList)


    def LoadFromDir(self, dbg = False):
        result = filedialog.askdirectory(title = "Select a Folder to import images")
        if result != "" :
            
            self.entryFolderName.set(result)
            print ("Loaded from: " + result)
            self.ImgDir = result + "/"
            self.imageFolderDir = [f for f in listdir(self.ImgDir) if re.match(r'.*\.png', f)]
            if len(self.imageFolderDir) == 0:
                messagebox.showinfo("Warning", "No png files in selected folder.")
            self.imageList = []
            for image in self.imageFolderDir:
                print(image)
                self.imageList.append(image)
                self.imgNameListStringVar.set(value = self.imageList)
            self.totalImgNumber = len(self.imageList)
            self.resultList = [""]*self.totalImgNumber
        else:
            messagebox.showinfo("Warning", "Folder not loaded")

    def LoadDir(self, dbg = False):
        self.imageFolderDir = listdir(self.initdir)
        self.imageList = []
        for image in self.imageFolderDir:
            print(image)
            self.imageList.append(image)
         
        #self.UpdateListboxImage()
        self.totalImgNumber = len(self.imageList)
        self.resultList = [""]*self.totalImgNumber
        self.imgNameListStringVar.set(value = self.imageList)
        
   # def UpdateListboxImage(self):
       


        #self.imageListbox.delete(0,END)
        #for image in self.imageList:
        #    self.imageListbox.insert(END, image)

if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.mainloop()
